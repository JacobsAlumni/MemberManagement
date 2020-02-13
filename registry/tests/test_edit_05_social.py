from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest


class EditSocialTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')
        self.obj = Alumni.objects.get(profile__username='Mounfem')

    def test_noedit(self):
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('edit_social', 'input_id_submit')

        # check that nothing happened
        self.assertEqual(self.current_url, reverse('edit_social'),
                         'Check that we stayed on the right page')

        # check that everything stayed the same
        self.assertEqual(self.obj.social.facebook,
                         'https://facebook.com/anna.freytag')
        self.assertEqual(self.obj.social.linkedin,
                         'https://www.linkedin.com/in/anna-freytag-1234578')
        self.assertEqual(self.obj.social.twitter,
                         'https://twitter.com/anna.freytag')
        self.assertEqual(self.obj.social.instagram,
                         'https://instagram.com/anna.freytag')
        self.assertEqual(self.obj.social.homepage, 'https://anna-freytag.com')

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

        # check that nothing happened
        self.assertEqual(self.current_url, reverse('edit_social'),
                         'Check that we stayed on the right page')

        # check that everything updated
        self.assertEqual(self.obj.social.facebook,
                         'https://facebook.com/freytag')
        self.assertEqual(self.obj.social.linkedin,
                         'https://www.linkedin.com/in/freytag-1234578')
        self.assertEqual(self.obj.social.twitter,
                         'https://twitter.com/freytag')
        self.assertEqual(self.obj.social.instagram,
                         'https://instagram.com/freytag')
        self.assertEqual(self.obj.social.homepage, 'https://freytag.com')

    def test_edit_empty(self):
        # enter nothing
        self.submit_form('edit_social', 'input_id_submit', send_form_keys={
            'id_facebook': '',
            'id_linkedin': '',
            'id_twitter': '',
            'id_instagram': '',
            'id_homepage': ''
        })

        # check that nothing happened
        self.assertEqual(self.current_url, reverse('edit_social'),
                         'Check that we stayed on the right page')

        # check that everything updated
        self.assertEqual(self.obj.social.facebook, None)
        self.assertEqual(self.obj.social.linkedin, None)
        self.assertEqual(self.obj.social.twitter, None)
        self.assertEqual(self.obj.social.instagram, None)
        self.assertEqual(self.obj.social.homepage, None)
