# ads/forms.py
from django import forms
from .models import Listing, Booking

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "location", "price_per_night"]
        # host/cover_image/type не трогаем — их нет в таблице

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["check_in", "check_out"]  # guest — это email, проставим во view