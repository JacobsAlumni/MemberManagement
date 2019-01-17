from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^token/', views.google_token_login, name='token_login')
]