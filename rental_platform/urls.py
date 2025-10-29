from django.contrib import admin
from django.urls import path, include
from ads.views import HomeView

# DRF Spectacular
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Web
    path("", HomeView.as_view(), name="home"),                          # главная
    path("", include(("users.urls", "users"), namespace="users")),      # login/register/logout
    path("ads/", include(("ads.urls", "ads"), namespace="ads")),        # всё из приложения ads
                                                                        # (внутри него есть router под /ads/api/)

    # OpenAPI схема и UI — привязаны к router из ads/urls.py
    path("ads/api/schema/", SpectacularAPIView.as_view(), name="ads-schema"),
    path(
        "ads/api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="ads-schema"),
        name="ads-swagger-ui",
    ),
    path(
        "ads/api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="ads-schema"),
        name="ads-redoc",
    ),
]