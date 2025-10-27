from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),

    # API вашего приложения объявлений (если есть)
    path("api/", include("ads.urls")),

    # Главная страница
    path("", home, name="home"),

    # Аутентификация: /register/ и /login/ берём из users/urls
    path("", include("users.urls")),
]