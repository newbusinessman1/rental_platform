from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views import View

from .forms import RegisterForm
from .models import Profile  # у тебя уже есть OneToOne Profile(user=...)


class RegisterView(View):
    template_name = "users/register.html"  # или "register.html" — как у тебя в шаблонах

    def get(self, request):
        return render(request, self.template_name, {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            # вернём форму с ошибками (занятый логин/почта, слабый пароль и т.п.)
            return render(request, self.template_name, {"form": form})

        # 1) создаём пользователя
        user = form.save(commit=False)  # создаёт User, но пока не пишет в БД
        user.first_name = form.cleaned_data["first_name"]
        user.last_name  = form.cleaned_data["last_name"]
        user.email      = form.cleaned_data["email"]
        user.save()  # теперь в БД

        # 2) роль и группы
        role = form.cleaned_data["role"]  # "host" | "guest"
        group_name = "Host" if role == "host" else "Guest"
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

        # 3) профиль (без дублей — берём существующий или создаём)
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = role
        profile.save()

        # 4) логиним и ведём домой
        login(request, user)
        messages.success(request, "Регистрация прошла успешно. Добро пожаловать!")
        return redirect("home")