from __future__ import annotations

from django.urls import path
from django.contrib import admin


from alumni.views import (
    ApprovalView,
    StatsViewApproved,
    StatsViewAll,
    StatsListView,
    preview_welcome_email,
    preview_welcomeback_password_email,
    preview_welcomeback_link_email,
)

urlpatterns = [
    path("approval/<int:id>/", ApprovalView.as_view(), name="approval_approval"),
    path(
        "approval/preview/welcome/<int:uid>/",
        preview_welcome_email,
        name="approval_welcomeemail",
    ),
    path(
        "approval/preview/welcomeback_password/<int:uid>/",
        preview_welcomeback_password_email,
        name="approval_welcomebackemail_password",
    ),
    path(
        "approval/preview/welcomeback_link/<int:uid>/",
        preview_welcomeback_link_email,
        name="approval_welcomebackemail_link",
    ),
    path("", admin.site.urls),
    path("stats/", StatsListView.as_view(), name="alumni_stats_index"),
    path("stats/all/", StatsViewAll.as_view(), name="alumni_stats_all"),
    path("stats/approved/", StatsViewApproved.as_view(), name="alumni_stats_approved"),
]
