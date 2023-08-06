from __future__ import annotations

from django.urls import path
from django.views import generic as generic_views
from . import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Login / Logout
    path(
        "login/",
        views.ClientIdLoginView.as_view(template_name="auth/login.html"),
        {},
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "token/sent/",
        generic_views.TemplateView.as_view(template_name="auth/token_sent.html"),
        name="token_sent",
    ),
    path("token/", views.google_token_login, name="token_login"),
    path("magic/", views.email_token_login, name="email_login"),
]
