from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from .integration import IntegrationTest

PORTAL_FIXED = [
    'portal',
    'edit',
    'edit_address',
    'edit_social',
    'edit_jacobs',
    'edit_job',
    'edit_skills',
    'edit_atlas',
]
PORTAL_SETUP_URLS = [
    'root',
    'root_register',
    'register',
    'setup',
    'setup_address',
    'setup_social',
    'setup_jacobs',
    'setup_job',
    'setup_skills',
    'setup_atlas',
    'setup_setup',
]
SETUP_PROTECTED_URLS = PORTAL_SETUP_URLS + PORTAL_FIXED + [
    'setup_membership',
    'setup_subscription',
    'update_subscription',
    'view_payments',
]


class AccessTest(IntegrationTest, StaticLiveServerTestCase):
    """ Checks that the homepage redirects appropriatly for the different stages of approval """

    def test_none(self):
        self.assert_url_follow('root', 'root')
        self.assert_url_follow('root_register', 'register')
        self.assert_url_follow('register', 'register')

        for url in SETUP_PROTECTED_URLS:
            if url in ['root', 'register', 'root_register']:
                continue
            self.assert_url_follow(url, 'login', new_url_reverse_get_params={'next': url})

    def test_setup_address(self):
        self.load_fixture('registry/tests/fixtures/signup_00_register.json')
        self.login('Mounfem')

        # check that all the protected urls go to the first page of the setup
        for url in SETUP_PROTECTED_URLS:
            self.assert_url_follow(url, 'setup_address')

    def test_setup_social(self):
        self.load_fixture('registry/tests/fixtures/signup_01_address.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assert_url_follow(url, 'setup_social')

    def test_setup_jacobs(self):
        self.load_fixture('registry/tests/fixtures/signup_02_social.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assert_url_follow(url, 'setup_jacobs')

    def test_setup_job(self):
        self.load_fixture('registry/tests/fixtures/signup_03_jacobs.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assert_url_follow(url, 'setup_job')

    def test_setup_skills(self):
        self.load_fixture('registry/tests/fixtures/signup_04_job.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assert_url_follow(url, 'setup_skills')

    def test_setup_atlas(self):
        self.load_fixture('registry/tests/fixtures/signup_05_skills.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assert_url_follow(url, 'setup_atlas')

    def test_setup_tier(self):
        self.load_fixture('registry/tests/fixtures/signup_06_atlas.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assert_url_follow(url, 'setup_membership')

    def test_setup_starter(self):
        self.load_fixture('registry/tests/fixtures/signup_07a_starter.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assert_url_follow(url, 'setup_setup')

    def test_setup_completed(self):
        self.load_fixture('registry/tests/fixtures/signup_09_finalize.json')
        self.login('Mounfem')

        for url in PORTAL_FIXED:
            self.assert_url_follow(url, url)

        for url in PORTAL_SETUP_URLS:
            self.assert_url_follow(url, 'portal')
