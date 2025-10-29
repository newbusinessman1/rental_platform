# ads/models.py
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


# ---------- Listing -> ads_listing ----------
class Listing(models.Model):
    class Meta:
        db_table = "ads_listing"
        managed = False  # НЕ трогаем существующую БД миграциями

    title = models.CharField(max_length=255, unique=True) #уникальное название
    slug = models.SlugField(max_length=255, unique=True, db_index=True, blank=True, null=True)
    description = models.TextField(blank=True)

    # В БД колонка city -> маппим на location
    location = models.CharField(max_length=255, db_column="city", blank=True, null=True)

    # В БД колонка именно price_per_night -> маппим корректно
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2,
                                          db_column="price_per_night", blank=True, null=True)

    # Эта колонка у меня есть в БД  — добавляем в модель
    created_at = models.DateTimeField(blank=True, null=True, db_column="created_at")

    owner_email = models.EmailField(db_column="owner_email", blank=True, default="")

    created_at = models.DateTimeField(db_column="created_at")

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

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_DECLINED = "declined"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_DECLINED, "Declined"),
    ]


    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    guest = models.EmailField(max_length=254, db_column="user_email")
    check_in = models.DateField(db_column="start_date")
    check_out = models.DateField(db_column="end_date")
    status = models.CharField(max_length=20, default=STATUS_PENDING, choices=STATUS_CHOICES)
    created_at = models.DateTimeField()  # есть в БД, берем как есть

    def __str__(self):
        return f"{self.guest} -> {self.listing} [{self.status}]"


# ---------- Review -> ads_review ----------
class Review(models.Model):
    class Meta:
        db_table = "ads_review"
        ordering = ["-created_at"]
        managed = False  # важное: не мигрируем эту таблицу

    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="reviews")
    user_email = models.CharField(max_length=255)
    rating = models.IntegerField()
    comment = models.TextField(db_column="comment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} → {self.listing} ({self.rating})"


# ---------- ViewHistory -> ads_viewhistory ----------
class ViewHistory(models.Model):
    class Meta:
        db_table = "ads_viewhistory"
        ordering = ["-created_at"]
        managed = False  # Django не меняет таблицу в БД

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column="viewed_at")  # ✅ авто-время
    ip_address = models.GenericIPAddressField(null=True, blank=True, db_column="ip")
    user_agent = models.TextField(blank=True)

    def __str__(self):
        return f"View {self.listing} at {self.created_at}"


