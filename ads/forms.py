# ads/forms.py
from django import forms
from .models import Listing, Booking, Review

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "location", "price_per_night", "owner_email"]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["check_in", "check_out"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 5)]),
            "comment": forms.Textarea(attrs={"rows": 4, "placeholder": "Как прошла поездка?"}),
        }