from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=120, db_index=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    owner_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELED = "canceled", "Canceled"

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    user_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews")
    user_email = models.EmailField()
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ViewHistory(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="views")
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
