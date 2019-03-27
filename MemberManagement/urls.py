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

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    # Static urls
    url(r'^imprint/$', TemplateView.as_view(template_name="static/imprint.html"), name='imprint'),
    url(r'^privacy/$', RedirectView.as_view(url='https://jacobs-alumni.de/privacy/', permanent=False), name='privacy'),

    # And recursively go into all the apps
    url(r'^admin/', include('alumni.urls')),
    url(r'^auth/', include('custom_auth.urls')),
    url(r'^atlas/', include('atlas.urls')),
    url(r'^payments/', include('payments.urls')),

    url(r'^', include('registry.urls'))
]
