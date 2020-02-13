from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from .integration import IntegrationTest

PORTAL_FIXED = [
    reverse('portal'),
    reverse('edit'),
    reverse('edit_address'),
    reverse('edit_social'),
    reverse('edit_jacobs'),
    reverse('edit_job'),
    reverse('edit_skills'),
    reverse('edit_atlas'),
]
PORTAL_SETUP_URLS = [
    reverse('root'),
    reverse('root_register'),
    reverse('register'),
    reverse('setup'),
    reverse('setup_address'),
    reverse('setup_social'),
    reverse('setup_jacobs'),
    reverse('setup_job'),
    reverse('setup_skills'),
    reverse('setup_atlas'),
    reverse('setup_setup'),
]
SETUP_PROTECTED_URLS = PORTAL_SETUP_URLS + PORTAL_FIXED + [
    reverse('setup_membership'),
    reverse('setup_subscription'),
    reverse('update_subscription'),
    reverse('view_payments'),
]


class HomeAccessTest(IntegrationTest, StaticLiveServerTestCase):
    """ Checks that the homepage redirects appropriatly for the different stages of approval """

    def test_none(self):
        ROOT = reverse('root')
        ROOT_REGISTER = reverse('root_register')
        REGISTER = reverse('register')

        self.assertEqual(self.sfollow('root', '.main-container'), ROOT)
        self.assertEqual(self.sfollow(
            'root_register', '.main-container'), REGISTER)
        self.assertEqual(self.sfollow('register',
                                      '.main-container'), REGISTER)

        for url in SETUP_PROTECTED_URLS:
            if url in [ROOT, ROOT_REGISTER, REGISTER]:
                continue
            self.assertEqual(self.sfollow(url, '.main-container'),
                             reverse('login')+'?next={}'.format(url), '{} redirects to login page'.format(url))

    def test_setup_address(self):
        self.load_fixture('registry/tests/fixtures/signup_00_register.json')
        self.login('Mounfem')

        # check that all the protected urls go to the first page of the setup
        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             reverse('setup_address'), '{} redirects to address setup'.format(url))

    def test_setup_social(self):
        self.load_fixture('registry/tests/fixtures/signup_01_address.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             reverse('setup_social'), '{} redirects to social setup'.format(url))

    def test_setup_jacobs(self):
        self.load_fixture('registry/tests/fixtures/signup_02_social.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             reverse('setup_jacobs'), '{} redirects to jacobs setup'.format(url))

    def test_setup_job(self):
        self.load_fixture('registry/tests/fixtures/signup_03_jacobs.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             reverse('setup_job'), '{} redirects to job setup'.format(url))

    def test_setup_skills(self):
        self.load_fixture('registry/tests/fixtures/signup_04_job.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             reverse('setup_skills'), '{} redirects to skills setup'.format(url))

    def test_setup_atlas(self):
        self.load_fixture('registry/tests/fixtures/signup_05_skills.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             reverse('setup_atlas'), '{} redirects to atlas setup'.format(url))

    def test_setup_tier(self):
        self.load_fixture('registry/tests/fixtures/signup_06_atlas.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             reverse('setup_membership'), '{} redirects to membership setup'.format(url))

    def test_setup_starter(self):
        self.load_fixture('registry/tests/fixtures/signup_07a_starter.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             reverse('setup_setup'), '{} redirects to completed setup'.format(url))

    def test_setup_completed(self):
        self.load_fixture('registry/tests/fixtures/signup_09_finalize.json')
        self.login('Mounfem')

        for url in PORTAL_FIXED:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             url, '{} does not redirect'.format(url))

        for url in PORTAL_SETUP_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             reverse('portal'), '{} redirects to portal home'.format(url))
