# ads/utils.py
from django.utils import timezone
from .models import Booking

def auto_finish_bookings():
    """
    Автоматически завершает брони, у которых дата выезда <= сегодня
    и статус = approved.
    """
    today = timezone.now().date()

    Booking.objects.filter(
        status=getattr(Booking, "STATUS_APPROVED", "approved"),
        end_date__lte=today
    ).update(status=getattr(Booking, "STATUS_FINISHED", "finished"))