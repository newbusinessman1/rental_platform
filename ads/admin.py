from django.contrib import admin
from .models import Listing, Booking, Review, ViewHistory

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "city", "price_per_night", "created_at")
    search_fields = ("title", "city")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user_email", "start_date", "end_date", "status", "created_at")
    list_filter = ("status",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user_email", "rating", "created_at")
    list_filter = ("rating",)

@admin.register(ViewHistory)
class ViewHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "ip", "viewed_at")
    list_filter = ("viewed_at",)
