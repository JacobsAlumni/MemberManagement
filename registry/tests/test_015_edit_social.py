from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest


class EditSocialTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Mounfem'

    def test_noedit(self):
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('edit_social', 'input_id_submit')
        self.assert_url_equal('edit_social')

        # check that everything stayed the same
        social = self.user.alumni.social
        self.assertEqual(social.facebook,
                         'https://facebook.com/anna.freytag')
        self.assertEqual(social.linkedin,
                         'https://www.linkedin.com/in/anna-freytag-1234578')
        self.assertEqual(social.twitter,
                         'https://twitter.com/anna.freytag')
        self.assertEqual(social.instagram,
                         'https://instagram.com/anna.freytag')
        self.assertEqual(social.homepage, 'https://anna-freytag.com')

    def test_edit_complete(self):
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('edit_social', 'input_id_submit', send_form_keys={
            'id_facebook': 'https://facebook.com/freytag',
            'id_linkedin': 'https://www.linkedin.com/in/freytag-1234578',
            'id_twitter': 'https://twitter.com/freytag',
            'id_instagram': 'https://instagram.com/freytag',
            'id_homepage': 'https://freytag.com'
        })
        self.assert_url_equal('edit_social')

        # check that everything updated
        social = self.user.alumni.social
        self.assertEqual(social.facebook,
                         'https://facebook.com/freytag')
        self.assertEqual(social.linkedin,
                         'https://www.linkedin.com/in/freytag-1234578')
        self.assertEqual(social.twitter,
                         'https://twitter.com/freytag')
        self.assertEqual(social.instagram,
                         'https://instagram.com/freytag')
        self.assertEqual(social.homepage, 'https://freytag.com')

    def test_edit_empty(self):
        # enter nothing
        self.submit_form('edit_social', 'input_id_submit', send_form_keys={
            'id_facebook': '',
            'id_linkedin': '',
            'id_twitter': '',
            'id_instagram': '',
            'id_homepage': ''
        })
        self.assert_url_equal('edit_social')

        # check that everything updated
        social = self.user.alumni.social
        self.assertEqual(social.facebook, None)
        self.assertEqual(social.linkedin, None)
        self.assertEqual(social.twitter, None)
        self.assertEqual(social.instagram, None)
        self.assertEqual(social.homepage, None)
