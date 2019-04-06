"""Registry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from .views import SignupView, SubscribeView, PaymentsView, UpdatePaymentView, PaymentsAdminView

urlpatterns = [
    url(r'^membership/$', SignupView.as_view(), name='setup_membership'),
    url(r'^subscribe/$', SubscribeView.as_view(), name='setup_subscription'),
    url(r'^update/$', UpdatePaymentView.as_view(), name='update_subscription'),
    url(r'^$', PaymentsView.as_view(), name='view_payments'),
    url(r'^admin/(?P<id>\d+)/$',
        PaymentsAdminView.as_view(), name='view_payments_admin'),
]
