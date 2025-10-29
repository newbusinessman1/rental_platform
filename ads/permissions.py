from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Booking

class IsAuthenticatedOrReadOnly(BasePermission):
    """Чтение всем, изменять — только аутентифицированным."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user and request.user.is_authenticated
        )

class IsListingOwnerOrReadOnly(BasePermission):
    """
    Редактировать Listing может только владелец (owner_email).
    Object-level проверка, чтобы browsable API не падал.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user_email = (getattr(request.user, "email", "") or "").strip().lower()
        return (obj.owner_email or "").strip().lower() == user_email

class IsHostOfBooking(BasePermission):
    """Approve/decline брони — только владелец объявления этой брони."""
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj: Booking):
        user_email = (getattr(request.user, "email", "") or "").strip().lower()
        owner = (getattr(obj.listing, "owner_email", "") or "").strip().lower()
        return owner == user_email