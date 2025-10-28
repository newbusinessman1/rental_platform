# ads/forms.py
from django import forms
from .models import Listing, Booking

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "location", "price_per_night"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full p-3 border rounded-lg"}),
            "description": forms.Textarea(attrs={"class": "w-full p-3 border rounded-lg", "rows": 4}),
            "location": forms.TextInput(attrs={"class": "w-full p-3 border rounded-lg"}),
            "price_per_night": forms.NumberInput(attrs={"class": "w-full p-3 border rounded-lg", "step": "0.01"}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["check_in", "check_out"]  # guest — это email, проставим во view