from __future__ import annotations

from django.conf.urls import url
from django.contrib import admin


from alumni.views import ApprovalView, preview_welcome_email, preview_welcomeback_password_email, preview_welcomeback_link_email

urlpatterns = [
    url(r'approval/(?P<id>\d+)/$', ApprovalView.as_view(), name='approval_approval'),
    url(r'approval/preview/welcome/(?P<uid>\d+)/$',
        preview_welcome_email, name='approval_welcomeemail'),
    url(r'approval/preview/welcomeback_password/(?P<uid>\d+)/$',
        preview_welcomeback_password_email, name='approval_welcomebackemail_password'),
    url(r'approval/preview/welcomeback_link/(?P<uid>\d+)/$',
        preview_welcomeback_link_email, name='approval_welcomebackemail_link'),
    url(r'^', admin.site.urls),
]
