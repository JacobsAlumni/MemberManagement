"""
Django Testing settings for MemberManagement project.
"""

from django_selenium_test import make_chrome_driver, make_firefox_driver

# import the default settings
from .settings import *

# No debug mode during testing, to be as close to production as possible
DEBUG = False
JS_TEST_MODE_FLAG = True

# Disable stripe keys in testing mode
STRIPE_SECRET_KEY = None
STRIPE_PUBLISHABLE_KEY = None
STRIPE_WEBHOOK_SECRET = 'useless-secret'

# enforce minimization for the tests
# so that we can test the production code
HTML_MINIFY = True

# Selenium test settings
from selenium import webdriver

headless = os.environ.get("SELENIUM_HEADLESS", "1") == "1"

SELENIUM_WEBDRIVERS = {
    'default': make_chrome_driver([], {}, headless=headless),
    'chrome': make_chrome_driver([], {}, headless=headless),
    'firefox': make_firefox_driver([], {}, headless=headless),
    'safari': {
        'callable': webdriver.Safari,
        'args': (),
        'kwargs': {},
    },
}
