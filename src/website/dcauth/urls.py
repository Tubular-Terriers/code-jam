from django.conf import settings
from django.urls import path

from . import views
from .views import todoHome

urlpatterns = [
    path("home/", views.Homepage, name="Homepage"),
    path("login/", views.login_via_discord, name="logindiscord"),
    path("success/", views.login_success, name="loginsuccess"),
    path("devlog/", views.login_success, name="loginsuccess"),
]
