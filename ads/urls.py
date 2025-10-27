# ads/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ListingViewSet, BookingViewSet, ReviewViewSet,
    PopularListingView, SearchStatsView, ViewHistoryView,
    HomeView, ListingDetailView,
    listing_create, booking_create, booking_success,
)

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),

    path('', HomeView.as_view(), name='home'),
    path('listing/new/', listing_create, name='listing_create'),
    path('listing/<slug:slug>/', ListingDetailView.as_view(), name='listing_detail'),
    path('listing/<slug:slug>/book/', booking_create, name='booking_create'),
    path('listing/<slug:slug>/book/success/', booking_success, name='booking_success'),

    path('popular-listings/', PopularListingView.as_view(), name='popular_listings'),
    path('search-stats/', SearchStatsView.as_view(), name='search_stats'),
    path('view-history/', ViewHistoryView.as_view(), name='view_history'),
]