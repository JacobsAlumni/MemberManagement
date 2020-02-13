from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest


class AtlasTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_05_skills.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')

    def test_signup_atlas_all(self):
        self.submit_form('setup_atlas', 'input_id_submit', select_checkboxes={
            'id_included': True,
            'id_birthdayVisible': True,
            'id_contactInfoVisible': True,
        })

        self.assertEqual(self.current_url, reverse('setup_membership'),
                         'Check that the user gets redirected to the membership page')

        obj = Alumni.objects.first().atlas
        self.assertEqual(obj.included, True)
        self.assertEqual(obj.birthdayVisible, True)
        self.assertEqual(obj.contactInfoVisible, True)

    def test_signup_atlas_birthday(self):
        self.submit_form('setup_atlas', 'input_id_submit', select_checkboxes={
            'id_included': True,
            'id_birthdayVisible': True,
            'id_contactInfoVisible': False,
        })

        self.assertEqual(self.current_url, reverse('setup_membership'),
                         'Check that the user gets redirected to the membership page')

        obj = Alumni.objects.first().atlas
        self.assertEqual(obj.included, True)
        self.assertEqual(obj.birthdayVisible, True)
        self.assertEqual(obj.contactInfoVisible, False)

    def test_signup_atlas_contact(self):
        self.submit_form('setup_atlas', 'input_id_submit', select_checkboxes={
            'id_included': True,
            'id_birthdayVisible': False,
            'id_contactInfoVisible': True,
        })

        self.assertEqual(self.current_url, reverse('setup_membership'),
                         'Check that the user gets redirected to the membership page')

        obj = Alumni.objects.first().atlas
        self.assertEqual(obj.included, True)
        self.assertEqual(obj.birthdayVisible, False)
        self.assertEqual(obj.contactInfoVisible, True)

    def test_signup_atlas_minimal(self):
        self.submit_form('setup_atlas', 'input_id_submit', select_checkboxes={
            'id_included': True,
            'id_birthdayVisible': False,
            'id_contactInfoVisible': False,
        })

        self.assertEqual(self.current_url, reverse('setup_membership'),
                         'Check that the user gets redirected to the membership page')

        obj = Alumni.objects.first().atlas
        self.assertEqual(obj.included, True)
        self.assertEqual(obj.birthdayVisible, False)
        self.assertEqual(obj.contactInfoVisible, False)

    def test_signup_atlas_empty(self):
        self.submit_form('setup_atlas', 'input_id_submit', select_checkboxes={
            'id_included': False,
            'id_birthdayVisible': False,
            'id_contactInfoVisible': False,
        })

        self.assertEqual(self.current_url, reverse('setup_membership'),
                         'Check that the user gets redirected to the membership page')

        obj = Alumni.objects.first().atlas
        self.assertEqual(obj.included, False)
        self.assertEqual(obj.birthdayVisible, False)
        self.assertEqual(obj.contactInfoVisible, False)
