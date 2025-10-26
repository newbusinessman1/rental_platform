from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # <── ДОБАВЬ

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("ads.urls")),
    path("api/users/", include("users.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("register/", TemplateView.as_view(template_name="register.html"), name="register_page"),
    path("login/",    TemplateView.as_view(template_name="login.html"),    name="login_page"),
]