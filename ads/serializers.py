from rest_framework import serializers
from .models import Listing, Booking, Review

# --- Listings ---
class ListingSerializer(serializers.ModelSerializer):
    reviews_count = serializers.IntegerField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id", "title", "slug", "description", "location",
            "price_per_night", "owner_email", "created_at",
            "reviews_count", "avg_rating",
        ]
        read_only_fields = ["slug", "owner_email", "created_at", "reviews_count", "avg_rating"]


# --- Bookings ---
class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source="listing.title", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id", "listing", "listing_title",
            "guest",
            "check_in", "check_out",
            "status", "created_at",
        ]
        read_only_fields = ["guest", "status", "created_at"]

    def validate(self, attrs):
        listing = attrs.get("listing") or getattr(self.instance, "listing", None)
        ci = attrs.get("check_in")
        co = attrs.get("check_out")

        if not (ci and co):
            raise serializers.ValidationError("Укажите даты заезда и выезда.")
        if ci >= co:
            raise serializers.ValidationError("Дата выезда должна быть позже даты заезда.")

        # Проверка пересечений
        from .models import Booking
        qs = Booking.objects.filter(listing=listing).exclude(pk=getattr(self.instance, "pk", None))
        overlap = qs.filter(
            check_in__lt=co,
            check_out__gt=ci,
            status__in=[
                getattr(Booking, "STATUS_PENDING", "pending"),
                getattr(Booking, "STATUS_APPROVED", "approved"),
            ],
        ).exists()
        if overlap:
            raise serializers.ValidationError("Эти даты уже заняты.")
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["guest"] = request.user.email or ""
        validated_data.setdefault("status", getattr(Booking, "STATUS_PENDING", "pending"))
        return super().create(validated_data)


# --- Reviews ---
class ReviewSerializer(serializers.ModelSerializer):
    # в модели: user_email, rating, comment, created_at
    class Meta:
        model = Review
        fields = ["id", "listing", "user_email", "rating", "comment", "created_at"]
        read_only_fields = ["user_email", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user_email"] = request.user.email or ""
        return super().create(validated_data)


# --- Вспомогательные сериализаторы для APIViews ---
class PopularListingItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.CharField()
    location = serializers.CharField(allow_null=True, allow_blank=True)
    price_per_night = serializers.DecimalField(max_digits=10, decimal_places=2)
    views_count = serializers.IntegerField()
    reviews_count = serializers.IntegerField()
    avg_rating = serializers.FloatField(allow_null=True)


class TypeCountSerializer(serializers.Serializer):
    type = serializers.CharField()
    cnt = serializers.IntegerField()


class LocationCountSerializer(serializers.Serializer):
    location = serializers.CharField(allow_null=True, allow_blank=True)
    cnt = serializers.IntegerField()


class SearchStatsSerializer(serializers.Serializer):
    by_type = TypeCountSerializer(many=True)
    top_locations = LocationCountSerializer(many=True)


class ViewHistoryItemSerializer(serializers.Serializer):
    listing = serializers.CharField()
    listing_id = serializers.IntegerField()
    user = serializers.CharField(allow_null=True)
    ip = serializers.CharField(allow_null=True)
    when = serializers.DateTimeField()