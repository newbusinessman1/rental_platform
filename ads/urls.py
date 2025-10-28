# ads/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ListingViewSet, BookingViewSet, ReviewViewSet,
    PopularListingView, SearchStatsView, ViewHistoryView,
    ListingDetailView, listing_create, booking_create, BookingSuccessView,
    MyListingsView, MyBookingsHostView, booking_approve, booking_decline, MyBookingsGuestView, booking_detail,
)

app_name = "ads"

# DRF router
router = DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = [
    # HTML
    path("listing/new/", listing_create, name="listing_create"),
    path("listing/<slug:slug>/", ListingDetailView.as_view(), name="listing_detail"),
    path("listing/<slug:slug>/book/", booking_create, name="booking_create"),
    path("listing/<slug:slug>/book/success/", BookingSuccessView.as_view(), name="booking_success"),

    path("my-listings/", MyListingsView.as_view(), name="my_listings"),
    path("host/bookings/", MyBookingsHostView.as_view(), name="my_bookings_host"),
    path("booking/<int:pk>/approve/", booking_approve, name="booking_approve"),
    path("booking/<int:pk>/decline/", booking_decline, name="booking_decline"),

    # простые JSON-эндоинты
    path("popular-listings/", PopularListingView.as_view(), name="popular_listings"),
    path("search-stats/", SearchStatsView.as_view(), name="search_stats"),
    path("view-history/", ViewHistoryView.as_view(), name="view_history"),

    #брони гостя в админке

    path("my-bookings/", MyBookingsGuestView.as_view(), name="my_bookings_guest"),
    path("booking/<int:pk>/", booking_detail, name="booking_detail"),

    # DRF под /ads/api/
    path("api/", include(router.urls)),
]