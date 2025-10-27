# rental_platform/urls.py
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from ads.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("ads.urls")),
    path("", HomeView.as_view(), name="home"),  # ← это главная страница
    # Аутентификация: /register/ и /login/ берём из users/urls
    path("", include("users.urls")),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
]