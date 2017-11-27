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
from django.contrib.auth import views as auth_views

from .views import registry as registry_views
from .views import setup as setup_views
from .views import edit as edit_views


urlpatterns = [
    # The Portal home page
    url(r'^$', registry_views.home, name='portal'),

    # Login / Logout
    url(r'^login/$', auth_views.login, {'template_name': 'auth/login.html'},
        name='login'),
    url('^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    # Registration
    url('^register/$', setup_views.register, name='register'),

    # Initial data Setup
    url(r'^setup/$', setup_views.setup, name='setup'),
    url(r'^setup/address/$', setup_views.address, name='setup_address'),
    url(r'^setup/jacobs/$', setup_views.jacobs, name='setup_jacobs'),
    url(r'^setup/social/$', setup_views.social, name='setup_social'),
    url(r'^setup/job/$', setup_views.job, name='setup_job'),

    # the portal for the user
    url(r'portal/', registry_views.portal, name='portal'),

    # Edit views
    url(r'^edit/$', edit_views.edit, name='edit'),
    url(r'^edit/address/$', edit_views.address, name='edit_address'),
    url(r'^edit/jacobs/$', edit_views.jacobs, name='edit_jacobs'),
    url(r'^edit/social/$', edit_views.social, name='edit_social'),
    url(r'^edit/job/$', edit_views.job, name='edit_job')
]
