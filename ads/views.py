from functools import wraps
from datetime import datetime as _dt, timedelta as _td

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Avg, Q, Exists, OuterRef
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, TemplateView

# DRF
from rest_framework import viewsets, permissions, generics, decorators, response
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ListingForm, BookingForm, ReviewForm
from .models import Listing, Booking, Review, ViewHistory
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from .permissions import (
    IsAuthenticatedOrReadOnly,
    IsListingOwnerOrReadOnly,
    IsHostOfBooking,
)


# ========= Публичные страницы =========


class HomeView(ListView):
    model = Listing
    template_name = "home.html"
    context_object_name = "listings"

    @staticmethod
    def _parse_date(s: str):
        from datetime import datetime
        if not s:
            return None
        for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                pass
        return None

    def get_queryset(self):
        from django.db.models import Count, Avg, Q, Exists, OuterRef
        q = (self.request.GET.get("q") or "").strip()
        check_in  = self._parse_date(self.request.GET.get("check_in"))
        check_out = self._parse_date(self.request.GET.get("check_out"))

        qs = (
            Listing.objects
            .annotate(
                reviews_count=Count("reviews"),
                avg_rating=Avg("reviews__rating"),
                views_count=Count("views"),   # <= ВСЕГДА есть в списке
            )
            .order_by("-id")
        )

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(location__icontains=q) |
                Q(description__icontains=q)
            )

        if check_in and check_out and check_in <= check_out:
            overlapping = Booking.objects.filter(listing_id=OuterRef("pk")).filter(
                Q(check_in__lte=check_out, check_out__gte=check_in) |
                Q(start_date__lte=check_out, end_date__gte=check_in)
            )
            qs = qs.annotate(has_overlap=Exists(overlapping)).filter(has_overlap=False)

        return qs

    def get_context_data(self, **kwargs):
        from django.db.models import Count, Q
        from datetime import timedelta
        ctx = super().get_context_data(**kwargs)

        # популярные по просмотрам за последние 30 дней
        since = timezone.now() - timedelta(days=30)
        popular = (
            Listing.objects
            .annotate(
                views_count=Count("views"),  # чтобы поле было и тут
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

    def get(self, request, *args, **kwargs):
        resp = super().get(request, *args, **kwargs)
        listing = self.get_object()
        # лог просмотра
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

        # ВАЖНО: в БД нет author_id — берём поля, которые есть
        ctx["reviews"] = (
            Review.objects
            .filter(listing=listing)
            .only("rating", "text", "created_at", "author_email")
            .order_by("-id")
        )

        ctx["booking_form"] = BookingForm()
        return ctx


@login_required
def review_create(request, slug):
    """
    Создать отзыв по листингу.
    Правила:
      - авторизован
      - есть approved бронь с прошедшей датой выезда
      - не оставлял отзыв ранее по этому листингу
    """
    listing = get_object_or_404(Listing, slug=slug)

    if not _booking_is_past_and_approved_for_user(listing, request.user):
        messages.error(request, "Оставлять отзывы можно только после подтверждённого проживания.")
        return redirect("ads:listing_detail", slug=listing.slug)

    if Review.objects.filter(listing=listing, author_email=(request.user.email or "")).exists():
        messages.info(request, "Вы уже оставляли отзыв для этого объявления.")
        return redirect("ads:listing_detail", slug=listing.slug)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            # в БД хранится email автора
            review.author_email = request.user.email or ""
            review.save()
            messages.success(request, "Спасибо! Ваш отзыв сохранён.")
            return redirect("ads:listing_detail", slug=listing.slug)
        messages.error(request, "Проверьте форму отзыва.")
    return redirect("ads:listing_detail", slug=listing.slug)


@login_required
def booking_create(request, slug):
    """Создать бронь по объявлению."""
    listing = get_object_or_404(Listing, slug=slug)

    # запрет владельцу бронировать свой объект
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

    # (опционально) можно переопределить perform_create/perform_update,
    # если хочешь автоматически проставлять owner_email = request.user.email
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
        serializer.save(author_email=(getattr(self.request.user, "email", "") or ""))


class PopularListingView(APIView):
    def get(self, request):
        qs = (
            Listing.objects
            .annotate(
                views_count=Count("views"),
                reviews_count=Count("reviews"),
                avg_rating=Avg("reviews__rating"),
            )
            .order_by("-views_count", "-reviews_count")[:10]
        )
        return Response(ListingSerializer(qs, many=True).data)


class SearchStatsView(APIView):
    def get(self, request):
        by_type = Listing.objects.values("type").annotate(cnt=Count("id")).order_by("-cnt")
        by_location = (
            Listing.objects.values("location").annotate(cnt=Count("id")).order_by("-cnt")[:10]
        )
        return Response({"by_type": list(by_type), "top_locations": list(by_location)})


class ViewHistoryView(generics.ListAPIView):
    queryset = ViewHistory.objects.select_related("listing", "user").order_by("-id")
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        data = [{
            "listing": vh.listing.title,
            "listing_id": vh.listing_id,
            "user": getattr(vh.user, "username", None),
            "ip": vh.ip_address,
            "when": vh.created_at,
        } for vh in self.get_queryset()[:200]]
        return Response(data)

# ========= Хост =========

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
    """Декоратор: не хост — 403; не залогинен — редирект на логин с next."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('users:login')}?next={request.get_full_path()}")
        if not is_host(request.user):
            raise PermissionDenied("Доступ разрешён только хостам.")
        return view_func(request, *args, **kwargs)
    return _wrapped

def _booking_is_past_and_approved_for_user(listing, user) -> bool:
    """Есть ли у пользователя approved-бронь по листингу с прошедшей датой выезда."""
    if not user.is_authenticated or not user.email:
        return False
    today = timezone.now().date()
    qs = Booking.objects.filter(
        listing=listing,
        guest__iexact=user.email,
        status=getattr(Booking, "STATUS_APPROVED", "approved"),
    )
    if hasattr(Booking, "end_date"):
        qs = qs.filter(end_date__lte=today)
    elif hasattr(Booking, "check_out"):
        qs = qs.filter(check_out__lte=today)
    else:
        return False
    return qs.exists()

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

def _same_email(a: str, b: str) -> bool:
    return (a or "").strip().lower() == (b or "").strip().lower()

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