"""
Django Testing settings for MemberManagement project.
"""

# import the default settings
from .settings import *

# No debug mode during testing, to be as close to production as possible
DEBUG = False
JS_TEST_MODE_FLAG = True

# Disable stripe keys in testing mode
STRIPE_SECRET_KEY = None
STRIPE_PUBLISHABLE_KEY = None

# enforce minimization for the tests
# so that we can test the production code
HTML_MINIFY = True

# Selenium test settings
from selenium import webdriver

if os.environ.get("SELENIUM_HEADLESS", "1") == "1":
    # chrome
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")

    # firefox
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")

else:
    chrome_options = None
    firefox_options = None

SELENIUM_WEBDRIVERS = {
    'default': {
        'callable': webdriver.Chrome,
        'args': (),
        'kwargs': {'options': chrome_options},
    },
    'firefox': {
        'callable': webdriver.Firefox,
        'args': (),
        'kwargs': {'options': firefox_options},
    },
    'safari': {
        'callable': webdriver.Safari,
        'args': (),
        'kwargs': {},
    },
}
