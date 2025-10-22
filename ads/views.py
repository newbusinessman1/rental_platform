from django.db.models import Count
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Listing, Booking, Review, ViewHistory
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer, ViewHistorySerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all().order_by("-id")
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by("-id")
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by("-id")
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]


class PopularListingView(generics.ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            Listing.objects
            .annotate(booking_count=Count("bookings"))
            .order_by("-booking_count", "-id")[:10]
        )


class SearchStatsView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        data = (
            Listing.objects.values("city")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
        return Response(list(data))


class ViewHistoryView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Ожидает JSON: { "listing": <id> }.
        IP и User-Agent вытянем из запроса.
        """
        listing_id = request.data.get("listing")
        if not listing_id:
            return Response({"detail": "listing is required"}, status=400)

        try:
            listing = Listing.objects.get(pk=listing_id)
        except Listing.DoesNotExist:
            return Response({"detail": "listing not found"}, status=404)

        entry = ViewHistory.objects.create(
            listing=listing,
            ip=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:512],
        )
        return Response(ViewHistorySerializer(entry).data, status=status.HTTP_201_CREATED)
