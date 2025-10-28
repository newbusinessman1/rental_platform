from django.contrib import admin
from django.urls import path, include
from ads.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),                 # единственный 'home'
    path("", include(("users.urls", "users"), namespace="users")),
    path("ads/", include(("ads.urls", "ads"), namespace="ads")),

    # если у тебя есть DRF-эндпоинты — держи их под /api/
    path("api/", include("ads.urls")),   # если такого файла нет — просто убери эту строку
]