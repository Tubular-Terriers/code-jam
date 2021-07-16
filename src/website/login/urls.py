from django.conf import settings
from django.urls import path

from . import views
from .views import todoHome

urlpatterns = [
    path("", todoHome.as_view(), name="todoHome"),
    path("login/", views.login_via_discord, name="logindiscord"),
    path("login-success/", views.login_success, name="loginsuccess"),
    # path('login/redirect',views.login_redirect,name='loginredirect'),
]
