# ads/serializers.py
from rest_framework import serializers
from .models import Listing, Booking, Review

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


class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source="listing.title", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "listing", "listing_title",
            "guest",
            "check_in", "check_out",
            "status", "created_at",
        ]
        read_only_fields = ["guest", "status", "created_at"]

    def validate(self, attrs):
        listing = attrs.get("listing") or getattr(self.instance, "listing", None)
        ci = attrs.get("check_in") or getattr(self.instance, "check_in", None)
        co = attrs.get("check_out") or getattr(self.instance, "check_out", None)

        if not (ci and co):
            raise serializers.ValidationError("Укажите даты заезда и выезда.")
        if ci >= co:
            raise serializers.ValidationError("Дата выезда должна быть позже даты заезда.")

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


# ads/serializers.py (фрагмент)

from rest_framework import serializers
from .models import Listing, Booking, Review

# ... ListingSerializer и BookingSerializer — без изменений ...

class ReviewSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source="listing.title", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id", "listing", "listing_title",
            "author_email", "rating", "created_at",
        ]
        read_only_fields = ["author_email", "created_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # показываем в API всегда ключ "comment"
        # если в модели есть поле comment — биндим напрямую,
        # иначе биндим на поле text.
        if hasattr(Review, "comment"):
            self.fields["comment"] = serializers.CharField()
            self._comment_field_name = "comment"
        else:
            self.fields["comment"] = serializers.CharField(source="text")
            self._comment_field_name = "text"

    def create(self, validated_data):
        # подставим email автора
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["author_email"] = request.user.email or ""

        # если пришёл ключ "comment", а в модели поле называется иначе — переложим
        if "comment" in validated_data and self._comment_field_name != "comment":
            validated_data[self._comment_field_name] = validated_data.pop("comment")

        return super().create(validated_data)