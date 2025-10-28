# ads/views.py
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Avg
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Listing, Booking, Review, ViewHistory
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from .forms import ListingForm, BookingForm
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login


class HomeView(ListView):
    model = Listing
    template_name = "home.html"
    context_object_name = "listings"

    def get_queryset(self):
        qs = (
            Listing.objects
            .annotate(
                reviews_count=Count("reviews"),
                avg_rating=Avg("reviews__rating"),
                views_count=Count("views"),
            )
            .order_by("-id")  # если вернёшь поле в модель: .order_by("-created_at")
        )
        return qs


def register(request):
    """Простая регистрация + авто-логин, потом редирект на главную."""
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
        ViewHistory.objects.create(
            listing=listing,
            user=request.user if request.user.is_authenticated else None,
            ip_address=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        )
        return resp

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["reviews"] = self.object.reviews.select_related("author").order_by("-id")
        ctx["booking_form"] = BookingForm()
        return ctx


@login_required
def listing_create(request):
    """Форма создания объявления (FBV)."""
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.host = request.user
            listing.owner_email = getattr(request.user, "email", "") or ""
            if not listing.created_at:
                listing.created_at = timezone.now()
            listing.save()
            return redirect("listing_detail", slug=listing.slug)
    else:
        form = ListingForm()
    return render(request, "ads/listing_form.html", {"form": form})


@login_required
def booking_create(request, slug):
    """Бронирование конкретного объявления (FBV)."""
    listing = get_object_or_404(Listing, slug=slug)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing
            # В БД колонка user_email (строка), маппится на поле guest:
            booking.guest = request.user.email or ""
            # В БД created_at NOT NULL — выставляем вручную:
            booking.created_at = timezone.now()
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

booking_success = BookingSuccessView.as_view()


# ===== API (как было) =====


class ListingViewSet(viewsets.ModelViewSet):
    serializer_class = ListingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Listing.objects.annotate(
            reviews_count=Count("reviews"),
            avg_rating=Avg("reviews__rating")
        ).order_by("-id")


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PopularListingView(APIView):
    def get(self, request):
        qs = Listing.objects.annotate(
            views_count=Count("views"),
            reviews_count=Count("reviews"),
            avg_rating=Avg("reviews__rating"),
        ).order_by("-views_count", "-reviews_count")[:10]
        return Response(ListingSerializer(qs, many=True).data)


class SearchStatsView(APIView):
    def get(self, request):
        by_type = (Listing.objects.values("type")
                   .annotate(cnt=Count("id")).order_by("-cnt"))
        by_location = (Listing.objects.values("location")
                       .annotate(cnt=Count("id")).order_by("-cnt")[:10])
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

def is_host(user):
    return user.is_authenticated and (user.groups.filter(name="Host").exists() or user.is_staff or user.is_superuser)

class MyListingsView(ListView):
    model = Listing
    template_name = "ads/my_listings.html"
    context_object_name = "listings"

    def get_queryset(self):
        email = self.request.user.email if self.request.user.is_authenticated else ""
        return (Listing.objects
                .filter(owner_email=email)
                .annotate(
                    reviews_count=Count("reviews"),
                    avg_rating=Avg("reviews__rating"),
                    views_count=Count("views"),
                )
                .order_by("-created_at", "-id"))


@login_required
@user_passes_test(is_host)
def listing_create(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            # заполняем поля, которых нет в форме, но обязательны в БД:
            if not listing.owner_email:
                listing.owner_email = request.user.email or ""
            if not listing.created_at:
                listing.created_at = timezone.now()

            # slug сгенерится в models.save(), если пустой
            listing.save()
            return redirect("listing_detail", slug=listing.slug)
    else:
        initial = {}
        if request.user.is_authenticated and request.user.email:
            initial["owner_email"] = request.user.email
        form = ListingForm(initial=initial)
    return render(request, "ads/listing_form.html", {"form": form})