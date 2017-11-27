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
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from .views import registry, setup, edit

urlpatterns = [
    # The Portal home page
    url(r'^$', registry.home, name='portal'),

    # TODO: The five portal edit views

    # Login / Logout
    url(r'^login/$', auth_views.login, name='login'),
    url('^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    # Registration and Initial Setup
    url('^register/$', registry.register, name='register'),
    url('^setup/$', setup.setup, name='setup'),

    # Edit views
    url(r'^edit/$', edit.edit),
    url(r'^edit/address/$', edit.address),
    url(r'^edit/jacobs/$', edit.jacobs),
    url(r'^edit/social/$', edit.social),
    url(r'^edit/job/$', edit.job)
]