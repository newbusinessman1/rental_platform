# ads/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, ReviewViewSet, PopularListingView, SearchStatsView, ViewHistoryView

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('popular-listings/', PopularListingView.as_view(), name='popular_listings'),
    path('search-stats/', SearchStatsView.as_view(), name='search_stats'),
    path('view-history/', ViewHistoryView.as_view(), name='view_history'),
]