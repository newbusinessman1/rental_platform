from rest_framework.permissions import BasePermission

def get_role(user):
    try:
        return user.profile.role
    except Exception:
        return 'guest'

class IsHostOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.is_authenticated and get_role(request.user) == 'host'
