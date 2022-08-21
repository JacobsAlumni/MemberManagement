"""
Django settings for MemberManagement project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from django.utils.translation import gettext_lazy as _
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wn_2m*p3v6i&+!cjf-%6j0yc1a3g2j%h@h865@=wcons^4skox'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
JS_TEST_MODE_FLAG = False
ENABLE_DEVEL_WARNING = True

ALLOWED_HOSTS = []

# Kosovo is missing from the list of countries
COUNTRIES_OVERRIDE = {
    'XK': _('Kosovo'),
}

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.auth',
    'django.contrib.sites',
    'registry',
    'cookielaw',
    'alumni',
    'custom_auth',
    'atlas',
    'payments',
    'donation_receipts',
    'donations',
    'impersonate',
    'django_forms_uikit',
    'django_countries',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpack_loader',
    'django_extensions',
    'rest_framework',
    'djmoney',
    'djmoney.contrib.exchange',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

ROOT_URLCONF = 'MemberManagement.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'MemberManagement', 'templates')), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'MemberManagement.context_processors.js_testmode_flag',
                'MemberManagement.context_processors.portal_version',
                'registry.context_processors.devel_warning',
                'payments.context_processors.stripe',
                'atlas.context_processors.atlas_allowed',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MemberManagement.wsgi.application'
ASGI_APPLICATION = 'MemberManagement.asgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")

LOGIN_URL = '/auth/login'
LOGOUT_URL = '/auth/logout'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

GSUITE_DOMAIN_NAME = 'jacobs-alumni.de'
GSUITE_OAUTH_CLIENT_ID = '118982546822-515a0fn0ldm96ebev0af5naj6qn8pt9i.apps.googleusercontent.com'

GSUITE_AUTH_FILE = os.environ.get("GSUITE_AUTH_FILE")
GSUITE_ADMIN_USER = 'admin@jacobs-alumni.de'
GSUITE_ORG_PATH = '/Approved Alumni'
GSUITE_PASS_LENGTH = 20

GSUITE_EMAIL_WELCOME_SUBJECT = 'Welcome to the Jacobs Alumni Association!'
GSUITE_EMAIL_WELCOMEBACK_SUBJECT = 'Welcome again to the Jacobs Alumni Association!'
GSUITE_EMAIL_ALL = ['membership@jacobs-alumni.de']

AUTHENTICATION_BACKENDS = [
    'sesame.backends.ModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'custom_auth.backend.GoogleTokenBackend'
]

SESAME_MAX_AGE = 300  # Emailed tokens expire after 5 minutes

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Django Channels settings
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = None
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
    os.path.join(BASE_DIR, "static"),
]


# webpack settings
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json')
    }
}

# Email settings
# https://docs.djangoproject.com/en/1.11/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587

EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_REPLY_TO = 'support@jacobs-alumni.de'
EMAIL_FROM = 'Alumni Association Portal <portal@portal.jacobs-alumni.de>'

# djmoney settings
CURRENCIES = ('EUR', 'USD')
BASE_CURRENCY = 'EUR'
EXCHANGE_BACKEND = 'djmoney.contrib.exchange.backends.FixerBackend'
FIXER_URL = 'https://api.exchangerate.host/latest?symbols=' + ','.join(CURRENCIES)
FIXER_ACCESS_KEY = 'dummy'

# Donation receipts settings
PDF_RENDER_SERVER = 'http://localhost:3000'
DONATION_RECEIPT_TEMPLATE = 'donation_receipts/receipt_pdf.html'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SIGNATURE_IMAGE = os.path.join(BASE_DIR, 'donation_receipts/sig.png')

# If true, will finalize donation receipts right when creating them
FINALIZE_AUTOMATICALLY = True

# Portal Version from file added during Docker build. Also present in dev env
try:
    with open(os.path.join(BASE_DIR, 'PORTAL_VERSION')) as f:
        PORTAL_VERSION = f.read()
except:
    PORTAL_VERSION = ''

# Import Local settings if available
try:
    from .local_settings import *
except ImportError:
    pass

SITE_ID = 1
