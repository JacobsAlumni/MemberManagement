from __future__ import annotations

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
from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie

from .views.registry import PortalView
from .views.vote import VoteLinkView, TokenExportView
from .views import setup as setup_views
from .views import edit as edit_views
from .views import api as api_views

urlpatterns = [
    # the portal for the user
    path("", PortalView.as_view(), name="portal"),
    path("vote/", VoteLinkView.as_view(), name="registry_vote"),
    path("vote/export/<int:id>/", TokenExportView.as_view(), name="registry_tokens"),
    # Registration
    path("register/", setup_views.RegisterView.as_view(), name="register"),
    path(
        "register/validate/",
        api_views.RegistrationValidationView.as_view(),
        name="register_validate",
    ),
    # Initial data Setup
    path("setup/", setup_views.SetupView.as_view(), name="setup"),
    path("setup/address/", setup_views.AddressSetup.as_view(), name="setup_address"),
    path("setup/social/", setup_views.SocialSetup.as_view(), name="setup_social"),
    path("setup/jacobs/", setup_views.JacobsSetup.as_view(), name="setup_jacobs"),
    path("setup/job/", setup_views.JobSetup.as_view(), name="setup_job"),
    path("setup/skills/", setup_views.SkillsSetup.as_view(), name="setup_skills"),
    path("setup/atlas/", setup_views.AtlasSetup.as_view(), name="setup_atlas"),
    path("setup/completed/", setup_views.CompletedSetup.as_view(), name="setup_setup"),
    # Edit views
    path("edit/", edit_views.edit, name="edit"),
    path("edit/address/", edit_views.address, name="edit_address"),
    path("edit/social/", edit_views.social, name="edit_social"),
    path("edit/jacobs/", edit_views.jacobs, name="edit_jacobs"),
    path("edit/job/", edit_views.job, name="edit_job"),
    path("edit/skills/", edit_views.skills, name="edit_skills"),
    path("edit/atlas/", edit_views.atlas, name="edit_atlas"),
]
