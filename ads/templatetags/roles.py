# ads/templatetags/roles.py
from django import template

register = template.Library()

@register.filter
def is_host(user):
    if not getattr(user, "is_authenticated", False):
        return False
    return (
        user.groups.filter(name="Host").exists()
        or user.is_staff
        or user.is_superuser
    )