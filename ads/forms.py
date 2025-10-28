# ads/forms.py
from django import forms
from .models import Listing, Booking, Review

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
        fields = ["check_in", "check_out"]
        widgets = {
            # ставим обычный текстовый инпут + класс для flatpickr
            "check_in":  forms.TextInput(attrs={"class": "datepicker w-full border rounded px-3 py-2", "placeholder": "Выберите дату заезда"}),
            "check_out": forms.TextInput(attrs={"class": "datepicker w-full border rounded px-3 py-2", "placeholder": "Выберите дату выезда"}),
        }

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    text = forms.CharField(
        label="Ваш отзыв",
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "Как прошла поездка?"})
    )

    class Meta:
        model = Review
        fields = ("rating", "text")
