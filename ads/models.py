# ads/models.py
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


# ---------- Listing -> ads_listing ----------
class Listing(models.Model):
    class Meta:
        db_table = "ads_listing"
        managed = False  # Базу не мигрируем

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, null=True)
    description = models.TextField(blank=True)

    # В БД колонка city -> маппим на location
    location = models.CharField(max_length=255, db_column="city", blank=True, null=True)

    # В БД колонка price_per_night
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2,
                                          db_column="price_per_night", blank=True, null=True)

    owner_email = models.EmailField(db_column="owner_email", blank=True, default="")

    # есть в БД колонка created_at
    created_at = models.DateTimeField(db_column="created_at", blank=True, null=True)

    def save(self, *args, **kwargs):
        # автослаг только если пусто
        if not self.slug:
            base = slugify(self.title) or f"listing-{self.pk or ''}".strip("-")
            cand = base or "listing"
            i = 1
            while Listing.objects.filter(slug=cand).exclude(pk=self.pk).exists():
                i += 1
                cand = f"{base}-{i}"
            self.slug = cand
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ---------- Booking -> ads_booking ----------
class Booking(models.Model):
    class Meta:
        db_table = "ads_booking"
        ordering = ["-created_at"]
        managed = False

    # статусы
    STATUS_PENDING  = "pending"
    STATUS_APPROVED = "approved"
    STATUS_DECLINED = "declined"
    STATUS_FINISHED = "finished"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_DECLINED, "Declined"),
        (STATUS_FINISHED, "Finished"),
    ]

    listing   = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    # в БД email гостя хранится в user_email
    guest     = models.EmailField(max_length=254, db_column="user_email")
    # даты называются start_date / end_date — маппим на check_in/check_out
    check_in  = models.DateField(db_column="start_date")
    check_out = models.DateField(db_column="end_date")
    status    = models.CharField(max_length=20, default=STATUS_PENDING, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(db_column="created_at")

    def __str__(self):
        return f"{self.guest} -> {self.listing} [{self.status}]"

    # Авто-завершение прошедших бронирований
    @classmethod
    def auto_finish_bookings(cls) -> int:
        """
        Все брони, у которых дата выезда прошла, переводим в 'finished',
        если они не уже finished или declined.
        Возвращает количество обновлённых строк.
        """
        today = timezone.now().date()
        filt = Q(check_out__lt=today) & ~Q(status=cls.STATUS_FINISHED) & ~Q(status=cls.STATUS_DECLINED)
        return cls.objects.filter(filt).update(status=cls.STATUS_FINISHED)


# ---------- Review -> ads_review ----------
class Review(models.Model):
    class Meta:
        db_table = "ads_review"
        ordering = ["-created_at"]
        managed = False  # таблицу не мигрируем

    listing     = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="reviews")
    user_email  = models.CharField(max_length=255)
    rating      = models.IntegerField()
    comment     = models.TextField(db_column="comment")
    created_at  = models.DateTimeField(db_column="created_at")

    def __str__(self):
        return f"{self.user_email} → {self.listing} ({self.rating})"


# ---------- ViewHistory -> ads_viewhistory ----------
class ViewHistory(models.Model):
    class Meta:
        db_table = "ads_viewhistory"
        ordering = ["-created_at"]
        managed = False

    listing    = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="views")
    user       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # в БД колонка viewed_at — сохраняем в поле created_at
    created_at = models.DateTimeField(auto_now_add=True, db_column="viewed_at")
    ip_address = models.GenericIPAddressField(null=True, blank=True, db_column="ip")
    user_agent = models.TextField(blank=True)

    def __str__(self):
        return f"View {self.listing} at {self.created_at}"