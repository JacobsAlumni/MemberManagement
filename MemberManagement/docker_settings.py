"""
Django Docker settings for MemberManagement project.
Reads all relevant setting from the environment
"""
from .settings import *
import sys

# No Debugging
DEBUG = False

# show a warning that this is not a real site
ENABLE_DEVEL_WARNING = os.environ.setdefault("DJANGO_ENABLE_DEVEL_WARNING", "") == "1"

# we want to allow all hosts
ALLOWED_HOSTS = os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "").split(",")

# all our sessions be safe
SECRET_KEY = os.environ.setdefault("DJANGO_SECRET_KEY", "")

# Passwords
DATABASES = {
    'default': {
        'ENGINE': os.environ.setdefault("DJANGO_DB_ENGINE", ""),
        'NAME': os.environ.setdefault("DJANGO_DB_NAME", ""),
        'USER': os.environ.setdefault("DJANGO_DB_USER", ""),
        'PASSWORD': os.environ.setdefault("DJANGO_DB_PASSWORD", ""),
        'HOST': os.environ.setdefault("DJANGO_DB_HOST", ""),
        'PORT': os.environ.setdefault("DJANGO_DB_PORT", ""),
    }
}

# add the stripe keys
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')

# update the client ID for Google login
GSUITE_OAUTH_CLIENT_ID = os.environ.setdefault("GSUITE_OAUTH_CLIENT_ID", "")

# add the static file root
STATIC_ROOT = "/var/www/static/"

# Sentry
if os.environ.get('DJANGO_RAVEN_DSN'):
    # add sentry
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )

    import os
    import raven

    RAVEN_CONFIG = {
        'dsn': os.environ.get('DJANGO_RAVEN_DSN')
    }
