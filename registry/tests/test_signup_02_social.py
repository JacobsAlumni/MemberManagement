from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest


class SocialTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_01_address.json']
    user = 'Mounfem'

    def test_signup_social_complete(self):
        self.submit_form('setup_social', 'input_id_submit', send_form_keys={
            'id_facebook': 'https://facebook.com/anna.freytag',
            'id_linkedin': 'https://www.linkedin.com/in/anna-freytag-1234578',
            'id_twitter': 'https://twitter.com/anna.freytag',
            'id_instagram': 'https://instagram.com/anna.freytag',
            'id_homepage': 'https://anna-freytag.com'
        })

        self.assert_url_equal('setup_jacobs',
                              'Check that the user gets redirected to the jacobs page')

        social = self.user.alumni.social
        self.assertEqual(social.facebook, 'https://facebook.com/anna.freytag')
        self.assertEqual(
            social.linkedin, 'https://www.linkedin.com/in/anna-freytag-1234578')
        self.assertEqual(social.twitter, 'https://twitter.com/anna.freytag')
        self.assertEqual(social.instagram, 'https://instagram.com/anna.freytag')
        self.assertEqual(social.homepage, 'https://anna-freytag.com')

    def test_signup_social_empty(self):
        self.submit_form('setup_social', 'input_id_submit', send_form_keys={
            'id_facebook': '',
            'id_linkedin': '',
            'id_twitter': '',
            'id_instagram': '',
            'id_homepage': ''
        })

        self.assert_url_equal('setup_jacobs',
                              'Check that the user gets redirected to the jacobs page')

        social = self.user.alumni.social
        self.assertEqual(social.facebook, None)
        self.assertEqual(social.linkedin, None)
        self.assertEqual(social.twitter, None)
        self.assertEqual(social.instagram, None)
        self.assertEqual(social.homepage, None)
