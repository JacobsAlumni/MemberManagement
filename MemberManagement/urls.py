from __future__ import annotations

"""MemberManagement URL Configuration

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
from django.views.generic import RedirectView, TemplateView

from .views import HomeView, HealthCheckDynamic, HealthCheckStatic

urlpatterns = [
    # Static Views
    url(r'^$', HomeView.as_view(), name='root'),
    url(r'^healthcheck/$', HealthCheckDynamic.as_view(), name='healthcheck'),
    url(r'^healthcheck/static/$', HealthCheckStatic.as_view(), name='healthcheck'),
    url(r'^imprint/$', RedirectView.as_view(url='https://jacobs-alumni.de/imprint/',
                                            permanent=False), name='imprint'),

    # Root redirects
    url(r'^register/$', RedirectView.as_view(pattern_name='register',
                                             permanent=False), name='root_register'),
    url(r'^privacy/$', RedirectView.as_view(url='https://jacobs-alumni.de/privacy/',
                                            permanent=False), name='privacy'),
    url(r'^vote/$', RedirectView.as_view(pattern_name='registry_vote',
                                             permanent=False), name='root_vote'),

    # And recursively go into all the apps
    url(r'^portal/', include('registry.urls')),
    url(r'^admin/', include('alumni.urls')),
    url(r'^impersonate/', include('impersonate.urls')),
    url(r'^auth/', include('custom_auth.urls')),
    url(r'^atlas/', include('atlas.urls')),
    url(r'^payments/', include('payments.urls')),
    url(r'^receipts/', include('donation_receipts.urls'))
]

# make an http 500 handler in case things go wrong
error_handler = TemplateView.as_view(template_name="base/error.html")
def handler500(request): return error_handler(request)
