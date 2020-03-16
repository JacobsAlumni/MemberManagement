from __future__ import annotations

from django.conf.urls import url

from .views import HomeView, SearchView, ProfileView

urlpatterns = [
    url(r'search/$', SearchView.as_view(), name='atlas_search'),
    url(r'profile/(?P<id>\d+)/$', ProfileView.as_view(), name='atlas_profile'),
    url(r'$', HomeView.as_view(), name='atlas_home'),
]
