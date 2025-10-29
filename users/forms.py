from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


ROLE_CHOICES = (
    ("guest", "Гость"),
    ("host", "Хост"),
)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=150, required=True)
    last_name  = forms.CharField(label="Фамилия", max_length=150, required=True)
    email      = forms.EmailField(label="Email", required=True)
    role       = forms.ChoiceField(label="Кем вы будете?", choices=ROLE_CHOICES, required=True)

    class Meta:
        model  = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "role",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует. Придумайте другой 🙂")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email