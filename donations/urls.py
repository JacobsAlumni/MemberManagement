from django.urls import path

from . import views

urlpatterns = [
    path('', views.DonateView.as_view(), name='donate'),
    path('<uuid:slug>', views.DonationSuccessView.as_view(), name='donation-detail'),
    path('failed', views.DonationFailedView.as_view(), name='donation-failed'),
]