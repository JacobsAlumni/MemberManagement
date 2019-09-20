from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .integration import IntegrationTest

PORTAL_FIXED = [
    '/portal/',
    '/portal/edit/',
    '/portal/edit/address/',
    '/portal/edit/social/',
    '/portal/edit/jacobs/',
    '/portal/edit/job/',
    '/portal/edit/skills/',
    '/portal/edit/atlas/'
]
PORTAL_SETUP_URLS = [
    '/',
    '/register/',
    '/portal/register/',
    '/portal/setup/',
    '/portal/setup/address/',
    '/portal/setup/social/',
    '/portal/setup/jacobs/',
    '/portal/setup/job/',
    '/portal/setup/skills/',
    '/portal/setup/atlas/',
    '/portal/setup/completed/'
]
SETUP_PROTECTED_URLS = PORTAL_SETUP_URLS + PORTAL_FIXED + [
    '/payments/membership/',
    '/payments/subscribe/',
    '/payments/update/',
    '/payments/'
]


class HomeAccessTest(IntegrationTest, StaticLiveServerTestCase):
    """ Checks that the homepage redirects appropriatly for the different stages of approval """

    def test_none(self):
        self.assertEqual(self.sfollow('/', '.main-container'), '/')
        self.assertEqual(self.sfollow(
            '/register/', '.main-container'), '/portal/register/')
        self.assertEqual(self.sfollow('/portal/register/',
                                      '.main-container'), '/portal/register/')

        for url in SETUP_PROTECTED_URLS:
            if url in ['/', '/register/', '/portal/register/']:
                continue
            self.assertEqual(self.sfollow(url, '.main-container'),
                             '/auth/login/?next={}'.format(url), '{} redirects to login page'.format(url))

    def test_setup_address(self):
        self.load_fixture('registry/tests/fixtures/signup_00_register.json')
        self.login('Mounfem')

        # check that all the protected urls go to the first page of the setup
        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             '/portal/setup/address/', '{} redirects to address setup'.format(url))

    def test_setup_social(self):
        self.load_fixture('registry/tests/fixtures/signup_01_address.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             '/portal/setup/social/', '{} redirects to social setup'.format(url))

    def test_setup_jacobs(self):
        self.load_fixture('registry/tests/fixtures/signup_02_social.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             '/portal/setup/jacobs/', '{} redirects to jacobs setup'.format(url))

    def test_setup_job(self):
        self.load_fixture('registry/tests/fixtures/signup_03_jacobs.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             '/portal/setup/job/', '{} redirects to job setup'.format(url))

    def test_setup_skills(self):
        self.load_fixture('registry/tests/fixtures/signup_04_job.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             '/portal/setup/skills/', '{} redirects to skills setup'.format(url))

    def test_setup_atlas(self):
        self.load_fixture('registry/tests/fixtures/signup_05_skills.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             '/portal/setup/atlas/', '{} redirects to atlas setup'.format(url))

    def test_setup_tier(self):
        self.load_fixture('registry/tests/fixtures/signup_06_atlas.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             '/payments/membership/', '{} redirects to membership setup'.format(url))

    def test_setup_starter(self):
        self.load_fixture('registry/tests/fixtures/signup_07a_starter.json')
        self.login('Mounfem')

        for url in SETUP_PROTECTED_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             '/portal/setup/completed/', '{} redirects to completed setup'.format(url))

    def test_setup_completed(self):
        self.load_fixture('registry/tests/fixtures/signup_08_finalize.json')
        self.login('Mounfem')

        for url in PORTAL_FIXED:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             url, '{} does not redirect'.format(url))

        for url in PORTAL_SETUP_URLS:
            self.assertEqual(self.sfollow(url, '.main-container'),
                             '/portal/', '{} redirects to portal home'.format(url))
