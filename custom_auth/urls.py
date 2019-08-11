from django.conf.urls import url
from django.views import generic as generic_views
from . import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Login / Logout
    url(r'^login/$', views.ClientIdLoginView.as_view(template_name='auth/login.html'), {}, name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^token/sent/', generic_views.TemplateView.as_view(
        template_name='auth/token_sent.html'), name='token_sent'),
    url(r'^token/', views.google_token_login, name='token_login'),
    url(r'^magic/', views.email_token_login, name='email_login'),
]
