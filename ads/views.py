# ads/views.py
from functools import wraps
from datetime import datetime as _dt, timedelta as _td
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import (
    ListingSerializer, BookingSerializer, ReviewSerializer,
    PopularListingItemSerializer, SearchStatsSerializer, ViewHistoryItemSerializer
)
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldDoesNotExist, PermissionDenied
from django.db.models import Avg, Count, Exists, OuterRef, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView

# DRF
from rest_framework import decorators, generics, permissions, response, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import BookingForm, ListingForm, ReviewForm
from .models import Booking, Listing, Review, ViewHistory
from .permissions import (
    IsAuthenticatedOrReadOnly,
    IsHostOfBooking,
    IsListingOwnerOrReadOnly,
)

from .utils import auto_finish_bookings


# ------------ утилиты ------------

def _has_field(model, name: str) -> bool:
    try:
        model._meta.get_field(name)
        return True
    except FieldDoesNotExist:
        return False


def is_host(user):
    """Хост — в группе 'Host' или staff/superuser."""
    return user.is_authenticated and (
        user.groups.filter(name="Host").exists() or user.is_staff or user.is_superuser
    )


def _is_owner(user, listing):
    """Сверка owner_email и user.email."""
    if not user.is_authenticated:
        return False
    owner_email = (listing.owner_email or "").strip().lower()
    user_email = (user.email or "").strip().lower()
    return bool(owner_email and user_email and owner_email == user_email)


def host_required(view_func):
    """Декоратор: не залогинен — редирект на логин; не хост — 403."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('users:login')}?next={request.get_full_path()}")
        if not is_host(request.user):
            raise PermissionDenied("Доступ разрешён только хостам.")
        return view_func(request, *args, **kwargs)
    return _wrapped


def _booking_is_past_and_approved_for_user(listing, user) -> bool:
    """
    Разрешаем отзыв, если у пользователя есть бронь по этому листингу,
    дата выезда уже наступила (<= сегодня), и статус либо approved, либо finished.
    Работает и с моделями, где поля дат называются check_in/check_out или start_date/end_date.
    """
    if not (getattr(user, "is_authenticated", False) and getattr(user, "email", "")):
        return False

    today = timezone.localdate()
    status_approved = getattr(Booking, "STATUS_APPROVED", "approved")
    status_finished = getattr(Booking, "STATUS_FINISHED", "finished")

    qs = Booking.objects.filter(
        listing=listing,
        guest__iexact=user.email,
        status__in=[status_approved, status_finished],
    )

    if hasattr(Booking, "check_out"):
        return qs.filter(check_out__lte=today).exists()
    elif hasattr(Booking, "end_date"):
        return qs.filter(end_date__lte=today).exists()
    return False


def _same_email(a: str, b: str) -> bool:
    return (a or "").strip().lower() == (b or "").strip().lower()


# ========= Публичные страницы =========

class HomeView(ListView):
    model = Listing
    template_name = "home.html"
    context_object_name = "listings"

    # аккуратно парсим дату из строки двух форматов
    @staticmethod
    def _parse_date(s: str):
        if not s:
            return None
        for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
            try:
                return _dt.strptime(s, fmt).date()
            except ValueError:
                continue
        return None

    def get_queryset(self):
        # при каждом заходе на главную завершаем просроченные approved → finished
        try:
            auto_finish_bookings()
        except Exception:
            # не валим страницу, если что-то не так с БД/соединением
            pass

        q = (self.request.GET.get("q") or "").strip()
        check_in = self._parse_date(self.request.GET.get("check_in"))
        check_out = self._parse_date(self.request.GET.get("check_out"))

        qs = (
            Listing.objects
            .annotate(
                reviews_count=Count("reviews"),
                avg_rating=Avg("reviews__rating"),
                views_count=Count("views"),
            )
            .order_by("-id")
        )

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(location__icontains=q) |
                Q(description__icontains=q)
            )

        # фильтрация по доступности — подстраиваемся под имена полей в Booking
        if check_in and check_out and check_in <= check_out:
            if _has_field(Booking, "check_in") and _has_field(Booking, "check_out"):
                start_f, end_f = "check_in", "check_out"
            elif _has_field(Booking, "start_date") and _has_field(Booking, "end_date"):
                start_f, end_f = "start_date", "end_date"
            else:
                start_f = end_f = None

            if start_f and end_f:
                overlapping = (
                    Booking.objects
                    .filter(listing_id=OuterRef("pk"))
                    .filter(Q(**{f"{start_f}__lte": check_out, f"{end_f}__gte": check_in}))
                )
                qs = qs.annotate(has_overlap=Exists(overlapping)).filter(has_overlap=False)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        since = timezone.now() - _td(days=30)
        popular = (
            Listing.objects
            .annotate(
                views_count=Count("views"),
                views_last30=Count("views", filter=Q(views__created_at__gte=since)),
            )
            .filter(views_last30__gt=0)
            .order_by("-views_last30", "-id")[:8]
        )
        ctx["popular_listings"] = list(popular)

        ctx["search"] = {
            "q": (self.request.GET.get("q") or "").strip(),
            "check_in": self._parse_date(self.request.GET.get("check_in")),
            "check_out": self._parse_date(self.request.GET.get("check_out")),
        }
        return ctx


def register(request):
    """Регистрация + авто-логин → главная."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


class ListingDetailView(DetailView):
    model = Listing
    template_name = "ads/listing_detail.html"
    context_object_name = "listing"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        slug_or_id = self.kwargs.get(self.slug_url_kwarg)
        if isinstance(slug_or_id, str) and slug_or_id.isdigit():
            return get_object_or_404(Listing, pk=int(slug_or_id))
        return get_object_or_404(Listing, slug=slug_or_id)

    def get(self, request, *args, **kwargs):
        # тоже аккуратно дофинишиваем просроченные
        try:
            auto_finish_bookings()
        except Exception:
            pass

        resp = super().get(request, *args, **kwargs)
        listing = self.object
        ViewHistory.objects.create(
            listing=listing,
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        )
        return resp

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        listing = self.object

        ctx["reviews"] = (
            Review.objects
            .filter(listing=listing)
            .only("user_email", "comment", "rating", "created_at")
            .order_by("-id")
        )

        # флаг — можно ли показывать форму отзыва
        ctx["can_review"] = _booking_is_past_and_approved_for_user(listing, self.request.user)
        ctx["review_form"] = ReviewForm() if ctx["can_review"] else None

        ctx["booking_form"] = BookingForm()
        return ctx



@login_required
def review_create(request, slug):
    """
    Создать отзыв по листингу.
    Разрешено, если есть бронь (approved/finished) с датой выезда <= сегодня
    и ранее отзыв по этому листингу не оставлялся.
    """
    listing = get_object_or_404(Listing, slug=slug)

    # доступ
    if not _booking_is_past_and_approved_for_user(listing, request.user):
        messages.error(request, "Оставлять отзывы можно только после подтверждённого проживания.")
        return redirect("ads:listing_detail", slug=listing.slug)

    # уже есть отзыв от этого e-mail для этого листинга?
    if Review.objects.filter(listing=listing, user_email=(request.user.email or "")).exists():
        messages.info(request, "Вы уже оставляли отзыв для этого объявления.")
        return redirect("ads:listing_detail", slug=listing.slug)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            # у модели поле называется user_email
            review.user_email = request.user.email or ""

            # На некоторых unmanaged таблицах auto_now_add не срабатывает корректно.
            # Подстрахуемся, чтобы не получить "created_at cannot be null".
            if hasattr(review, "created_at") and not review.created_at:
                review.created_at = timezone.now()

            # (подстраховка) если вдруг шаблон прислал другое имя поля — добьём руками
            if not getattr(review, "comment", None):
                review.comment = (request.POST.get("comment") or
                                  request.POST.get("text") or "").strip()

            review.save()
            messages.success(request, "Спасибо! Ваш отзыв сохранён.")
            return redirect("ads:listing_detail", slug=listing.slug)
        else:
            messages.error(request, "Проверьте форму отзыва.")

    return redirect("ads:listing_detail", slug=listing.slug)


@login_required
def booking_create(request, slug):
    """Создать бронь по объявлению (HTML)."""
    listing = get_object_or_404(Listing, slug=slug)

    if _is_owner(request.user, listing):
        messages.error(request, "Вы не можете бронировать собственное объявление.")
        return redirect("ads:listing_detail", slug=listing.slug)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing
            booking.guest = request.user.email or ""
            booking.created_at = timezone.now()
            booking.status = getattr(Booking, "STATUS_PENDING", "pending")
            booking.save()
            return redirect("ads:booking_success", slug=listing.slug)
    else:
        form = BookingForm()
    return render(request, "ads/booking_form.html", {"form": form, "listing": listing})


class BookingSuccessView(TemplateView):
    template_name = "ads/booking_success.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        if slug:
            ctx["listing"] = get_object_or_404(Listing, slug=slug)
        return ctx


# ========= API (DRF) =========

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsListingOwnerOrReadOnly]

    def perform_create(self, serializer):
        owner_email = (getattr(self.request.user, "email", "") or "")
        serializer.save(owner_email=owner_email or serializer.validated_data.get("owner_email", ""))


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("listing")
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(guest=getattr(self.request.user, "email", "") or "")

    @decorators.action(
        detail=True, methods=["post"],
        permission_classes=[permissions.IsAuthenticated, IsHostOfBooking]
    )
    def approve(self, request, pk=None):
        booking = self.get_object()
        booking.status = getattr(Booking, "STATUS_APPROVED", "approved")
        booking.save(update_fields=["status"])
        return response.Response({"status": booking.status})

    @decorators.action(
        detail=True, methods=["post"],
        permission_classes=[permissions.IsAuthenticated, IsHostOfBooking]
    )
    def decline(self, request, pk=None):
        booking = self.get_object()
        booking.status = getattr(Booking, "STATUS_DECLINED", "declined")
        booking.save(update_fields=["status"])
        return response.Response({"status": booking.status})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("listing")
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user_email=(getattr(self.request.user, "email", "") or ""))


class PopularListingView(APIView):
    @extend_schema(
        responses={200: PopularListingItemSerializer(many=True)},
        description="Топ-10 листингов по просмотрам/отзывам"
    )
    def get(self, request):
        from django.db.models import Count, Avg
        qs = (
            Listing.objects
            .annotate(
                views_count=Count("views"),
                reviews_count=Count("reviews"),
                avg_rating=Avg("reviews__rating"),
            )
            .order_by("-views_count", "-reviews_count")[:10]
            .values("id", "title", "slug", "location", "price_per_night",
                    "views_count", "reviews_count", "avg_rating")
        )
        return Response(list(qs))


class SearchStatsView(APIView):
    @extend_schema(
        responses={200: SearchStatsSerializer},
        description="Агрегированная статистика по типам и топ-локациям"
    )
    def get(self, request):
        from django.db.models import Count
        by_type = list(Listing.objects.values("type").annotate(cnt=Count("id")).order_by("-cnt"))
        top_locations = list(
            Listing.objects.values("location").annotate(cnt=Count("id")).order_by("-cnt")[:10]
        )
        return Response({"by_type": by_type, "top_locations": top_locations})


class ViewHistoryView(generics.ListAPIView):
    queryset = ViewHistory.objects.select_related("listing", "user").order_by("-id")
    permission_classes = [permissions.AllowAny]
    serializer_class = ViewHistoryItemSerializer  # <-- ВАЖНО для drf-spectacular

    @extend_schema(responses={200: ViewHistoryItemSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        data = [{
            "listing": vh.listing.title,
            "listing_id": vh.listing_id,
            "user": getattr(vh.user, "username", None),
            "ip": vh.ip_address,
            "when": vh.created_at,
        } for vh in self.get_queryset()[:200]]
        return Response(data)


# ========= Кабинеты / таблицы =========

class MyListingsView(ListView):
    """Список объявлений текущего пользователя (как хоста)."""
    model = Listing
    template_name = "ads/my_listings.html"
    context_object_name = "listings"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Listing.objects.none()
        email = (user.email or "").strip()
        return (
            Listing.objects
            .filter(owner_email__iexact=email)
            .annotate(
                reviews_count=Count("reviews"),
                avg_rating=Avg("reviews__rating"),
                views_count=Count("views"),
            )
            .order_by("-created_at", "-id")
        )


class MyBookingsGuestView(LoginRequiredMixin, ListView):
    """Брони, которые создал текущий пользователь как гость."""
    model = Booking
    template_name = "ads/my_bookings_guest.html"
    context_object_name = "bookings"

    def get_queryset(self):
        email = (self.request.user.email or "").strip()
        if not email:
            return Booking.objects.none()
        return (
            Booking.objects
            .select_related("listing")
            .filter(guest__iexact=email)
            .order_by("-created_at", "-id")
        )


class MyBookingsHostView(ListView):
    """Все брони по объявлениям текущего хоста."""
    model = Booking
    template_name = "ads/my_bookings_host.html"
    context_object_name = "bookings"

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Booking.objects.none()
        email = (user.email or "").strip()
        return (
            Booking.objects
            .select_related("listing")
            .filter(listing__owner_email__iexact=email)
            .order_by("-created_at", "-id")
        )


@login_required
def booking_detail(request, pk: int):
    """Детали бронирования (гость-инициатор, владелец листинга или staff/superuser)."""
    booking = get_object_or_404(Booking.objects.select_related("listing"), pk=pk)
    user = request.user
    can_view = (
        _same_email(booking.guest, getattr(user, "email", "")) or
        _same_email(getattr(booking.listing, "owner_email", ""), getattr(user, "email", "")) or
        user.is_staff or user.is_superuser
    )
    if not can_view:
        raise Http404("Booking not found")
    return render(request, "ads/booking_detail.html", {"booking": booking})


@login_required
def booking_approve(request, pk):
    """Подтвердить бронь (HTML-версия, только владелец)."""
    booking = get_object_or_404(Booking.objects.select_related("listing"), pk=pk)
    if not _is_owner(request.user, booking.listing):
        messages.error(request, "Нет прав: это не ваше объявление.")
        return redirect("ads:my_bookings_host")
    if request.method == "POST":
        booking.status = getattr(Booking, "STATUS_APPROVED", "approved")
        booking.save(update_fields=["status"])
        messages.success(request, "Бронь подтверждена.")
    return redirect("ads:my_bookings_host")


@login_required
def booking_decline(request, pk):
    """Отклонить бронь (HTML-версия, только владелец)."""
    booking = get_object_or_404(Booking.objects.select_related("listing"), pk=pk)
    if not _is_owner(request.user, booking.listing):
        messages.error(request, "Нет прав: это не ваше объявление.")
        return redirect("ads:my_bookings_host")
    if request.method == "POST":
        booking.status = getattr(Booking, "STATUS_DECLINED", "declined")
        booking.save(update_fields=["status"])
        messages.success(request, "Бронь отклонена.")
    return redirect("ads:my_bookings_host")


@host_required
def listing_create(request):
    """Создание объявления — только для хостов."""
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            if not listing.owner_email:
                listing.owner_email = request.user.email or ""
            if not listing.created_at:
                listing.created_at = timezone.now()
            listing.save()
            return redirect("ads:listing_detail", slug=listing.slug)
    else:
        initial = {}
        if request.user.is_authenticated and request.user.email:
            initial["owner_email"] = request.user.email
        form = ListingForm(initial=initial)
    return render(request, "ads/listing_form.html", {"form": form})