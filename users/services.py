# users/services.py
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ads.models import Listing, Booking, Review

HOSTS = "Hosts"
GUESTS = "Guests"

def ensure_groups():
    """Создаёт группы и даёт им нужные права, если ещё не созданы."""
    hosts, _ = Group.objects.get_or_create(name=HOSTS)
    guests, _ = Group.objects.get_or_create(name=GUESTS)

    # права для объявлений
    ct_listing = ContentType.objects.get_for_model(Listing)
    can_add_listing = Permission.objects.get(codename="add_listing", content_type=ct_listing)
    can_change_listing = Permission.objects.get(codename="change_listing", content_type=ct_listing)
    can_delete_listing = Permission.objects.get(codename="delete_listing", content_type=ct_listing)
    can_view_listing = Permission.objects.get(codename="view_listing", content_type=ct_listing)

    # права для бронирований
    ct_booking = ContentType.objects.get_for_model(Booking)
    can_add_booking = Permission.objects.get(codename="add_booking", content_type=ct_booking)
    can_view_booking = Permission.objects.get(codename="view_booking", content_type=ct_booking)

    # права для отзывов
    ct_review = ContentType.objects.get_for_model(Review)
    can_add_review = Permission.objects.get(codename="add_review", content_type=ct_review)
    can_view_review = Permission.objects.get(codename="view_review", content_type=ct_review)

    # Хост: CRUD на объявления + просмотр бронирований/отзывов
    hosts.permissions.set({
        can_add_listing, can_change_listing, can_delete_listing, can_view_listing,
        can_view_booking, can_view_review,
    })

    # Гость: бронирование + отзывы + просмотр объявлений
    guests.permissions.set({
        can_add_booking, can_view_booking,
        can_add_review,  can_view_review,
        can_view_listing,
    })

    return hosts, guests


def set_user_role(user, role: str):
    """Ставит профильную роль и кидает пользователя в нужную группу."""
    hosts, guests = ensure_groups()

    # Обновляем профиль
    profile = getattr(user, "profile", None)
    if profile:
        profile.role = role
        profile.save(update_fields=["role"])

    # Чистим старые группы и добавляем нужную
    user.groups.remove(hosts, guests)
    if role == "host":
        user.groups.add(hosts)
    else:
        user.groups.add(guests)
