from django.conf.urls import url
from django.contrib import admin


from alumni.views import ApprovalView

urlpatterns = [
    url(r'approval/(?P<id>\d+)/$', ApprovalView.as_view(), name='approval_approval'),
    url(r'^', admin.site.urls),
]
