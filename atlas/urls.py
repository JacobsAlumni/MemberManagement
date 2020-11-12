from __future__ import annotations

from django.urls import path

from .views import HomeView, SearchView, ProfileView

urlpatterns = [
    path('search/', SearchView.as_view(), name='atlas_search'),
    path('profile/<int:id>/', ProfileView.as_view(), name='atlas_profile'),
    path('', HomeView.as_view(), name='atlas_home'),
]
