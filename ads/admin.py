# ads/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count, Avg
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Listing, Booking, Review, ViewHistory
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer
from .forms import ListingForm, BookingForm


# ===== HTML =====

class HomeView(ListView):
    model = Listing
    template_name = "home.html"
    context_object_name = "listings"

    def get_queryset(self):
        return (Listing.objects
                .annotate(
                    reviews_count=Count("reviews"),
                    avg_rating=Avg("reviews__rating"),
                    views_count=Count("views"),
                )
                .order_by("-created_at"))


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
        ctx["reviews"] = self.object.reviews.select_related("author").order_by("-created_at")
        ctx["booking_form"] = BookingForm()
        return ctx


@login_required
def listing_create(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            # host убери, если в БД такого столбца нет
            # listing.host = request.user
            listing.save()
            return redirect("listing_detail", slug=listing.slug)
    else:
        form = ListingForm()
    return render(request, "ads/listing_form.html", {"form": form})


@login_required
def booking_create(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.listing = listing
            # у тебя guest = EmailField (db_column='user_email')
            # поэтому пишем email, а не объект пользователя
            if request.user.is_authenticated and getattr(request.user, "email", None):
                booking.guest = request.user.email
            booking.save()
            return redirect("booking_success", slug=listing.slug)
    else:
        form = BookingForm()
    return render(request, "ads/booking_form.html", {"form": form, "listing": listing})


class BookingSuccessView(TemplateView):
    template_name = "ads/booking_success.html"

booking_success = BookingSuccessView.as_view()


# ===== API =====

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
        # guest — это email-строка
        email = self.request.user.email if self.request.user.is_authenticated else ""
        serializer.save(guest=email)


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
        # УБРАЛИ .values("type") — такого столбца в БД нет
        top_locations = (Listing.objects.values("location")
                         .annotate(cnt=Count("id"))
                         .order_by("-cnt")[:10])
        return Response({"top_locations": list(top_locations)})


class ViewHistoryView(generics.ListAPIView):
    queryset = ViewHistory.objects.select_related("listing", "user").order_by("-created_at")
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