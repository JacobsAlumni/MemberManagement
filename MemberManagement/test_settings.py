"""
Django Testing settings for MemberManagement project.
"""

# import the default settings
from .settings import *

# enforce minimization for the tests
# so that we can test the production code
HTML_MINIFY = True

# Selenium test settings
from selenium import webdriver

SELENIUM_HEADLESS = os.environ.get("SELENIUM_HEADLESS", "1") == "1"
if SELENIUM_HEADLESS:
    os.environ['MOZ_HEADLESS'] = '1'
SELENIUM_WEBDRIVERS = {
    'default': {
        'callable': webdriver.Firefox,
        'args': (),
        'kwargs': {},
    }
}
