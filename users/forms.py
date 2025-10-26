from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, initial=Profile.ROLE_GUEST)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # профиль уже создан сигналом — обновим роль и триггернём sync_groups_with_role
            user.profile.role = self.cleaned_data["role"]
            user.profile.save()
        return user