from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest

from alumni.models import Alumni

class SocialTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_01_address.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')

    def test_signup_social_complete(self):
        self.submit_form('/portal/setup/social/', 'input_id_submit', send_form_keys={
            'id_facebook': 'https://facebook.com/anna.freytag',
            'id_linkedin': 'https://www.linkedin.com/in/anna-freytag-1234578',
            'id_twitter': 'https://twitter.com/anna.freytag',
            'id_instagram': 'https://instagram.com/anna.freytag',
            'id_homepage': 'https://anna-freytag.com'
        })

        self.assertEqual(self.current_url, '/portal/setup/jacobs/',
                         'Check that the user gets redirected to the jacobs page')

        obj = Alumni.objects.first().social
        self.assertEqual(obj.facebook, 'https://facebook.com/anna.freytag')
        self.assertEqual(obj.linkedin, 'https://www.linkedin.com/in/anna-freytag-1234578')
        self.assertEqual(obj.twitter, 'https://twitter.com/anna.freytag')
        self.assertEqual(obj.instagram, 'https://instagram.com/anna.freytag')
        self.assertEqual(obj.homepage, 'https://anna-freytag.com')

    def test_signup_social_empty(self):
        self.submit_form('/portal/setup/social/', 'input_id_submit', send_form_keys={
            'id_facebook': '',
            'id_linkedin': '',
            'id_twitter': '',
            'id_instagram': '',
            'id_homepage': ''
        })

        self.assertEqual(self.current_url, '/portal/setup/jacobs/',
                         'Check that the user gets redirected to the jacobs page')

        obj = Alumni.objects.first().social
        self.assertEqual(obj.facebook, None)
        self.assertEqual(obj.linkedin, None)
        self.assertEqual(obj.twitter, None)
        self.assertEqual(obj.instagram, None)
        self.assertEqual(obj.homepage, None)
