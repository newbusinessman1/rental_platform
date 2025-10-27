# ads/serializers.py
from rest_framework import serializers
from .models import Listing, Booking, Review, ViewHistory

class ListingSerializer(serializers.ModelSerializer):
    reviews_count = serializers.IntegerField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id", "title", "slug", "description", "location",
            "price_per_night", "type", "cover_image", "host",
            "created_at", "reviews_count", "avg_rating",
        ]
        read_only_fields = ("slug", "host", "created_at")

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "listing", "guest", "check_in", "check_out", "status", "created_at"]
        read_only_fields = ("created_at",)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "listing", "author", "rating", "text", "created_at"]
        read_only_fields = ("author", "created_at")

class ViewHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewHistory
        fields = ["id", "listing", "user", "ip_address", "user_agent", "created_at"]
        read_only_fields = ("created_at",)