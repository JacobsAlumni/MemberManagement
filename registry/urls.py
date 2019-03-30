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

from .views import registry as registry_views
from .views import setup as setup_views
from .views import edit as edit_views

urlpatterns = [

    # the portal for the user
    url(r'^$', registry_views.portal, name='portal'),

    # Registration
    url(r'^register/$', setup_views.RegisterView.as_view(), name='register'),

    # Initial data Setup
    url(r'^setup/$', setup_views.SetupView.as_view(), name='setup'),
    url(r'^setup/address/$', setup_views.AddressSetup.as_view(), name='setup_address'),
    url(r'^setup/social/$', setup_views.SocialSetup.as_view(), name='setup_social'),
    url(r'^setup/jacobs/$', setup_views.JacobsSetup.as_view(), name='setup_jacobs'),
    url(r'^setup/job/$', setup_views.JobSetup.as_view(), name='setup_job'),
    url(r'^setup/skills/$', setup_views.SkillsSetup.as_view(), name='setup_skills'),
    url(r'^setup/atlas/$', setup_views.AtlasSetup.as_view(), name='setup_atlas'),

    # Edit views
    url(r'^edit/$', edit_views.edit, name='edit'),
    url(r'^edit/address/$', edit_views.address, name='edit_address'),
    url(r'^edit/social/$', edit_views.social, name='edit_social'),
    url(r'^edit/jacobs/$', edit_views.jacobs, name='edit_jacobs'),
    url(r'^edit/job/$', edit_views.job, name='edit_job'),
    url(r'^edit/skills/$', edit_views.skills, name='edit_skills'),
    url(r'^edit/atlas/$', edit_views.atlas, name='edit_atlas'),
]
