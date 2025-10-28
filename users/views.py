# users/views.py
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm
from .models import Profile


class RegisterView(View):
    template_name = "users/register.html"

    def get(self, request):
        return render(request, self.template_name, {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 1) создаём пользователя
            user = form.save(commit=False)
            user.first_name = form.cleaned_data["first_name"]
            user.last_name  = form.cleaned_data["last_name"]
            user.email      = form.cleaned_data["email"]
            user.save()

            # 2) добавляем в группу по роли
            role = form.cleaned_data["role"]  # 'host' | 'guest'
            group_name = "Host" if role == "host" else "Guest"
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

            # 3) профиль — безопасно (не упадёт, если уже есть)
            Profile.objects.get_or_create(user=user, defaults={"role": role})

            # 4) логиним и уводим на главную (PRG-паттерн)
            login(request, user)
            return redirect("home")

        # если форма с ошибками — показать их
        return render(request, self.template_name, {"form": form})

