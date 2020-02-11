from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest


class EditAtlasTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')
        self.obj = Alumni.objects.get(profile__username='Mounfem')

    def test_noedit(self):
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('/portal/edit/atlas/', 'input_id_submit')

        # check that nothing happened
        self.assertEqual(self.current_url, '/portal/edit/atlas/',
                         'Check that we stayed on the right page')

        # check that everything stayed the same
        self.assertEqual(self.obj.atlas.included, True)
        self.assertEqual(self.obj.atlas.birthdayVisible, True)
        self.assertEqual(self.obj.atlas.contactInfoVisible, True)

    def test_signup_atlas_birthday(self):
        self.submit_form('/portal/edit/atlas/', 'input_id_submit', select_checkboxes={
            'id_included': True,
            'id_birthdayVisible': True,
            'id_contactInfoVisible': False,
        })

        self.assertEqual(self.current_url, '/portal/edit/atlas/',
                         'Check that we stayed on the right page')

        self.assertEqual(self.obj.atlas.included, True)
        self.assertEqual(self.obj.atlas.birthdayVisible, True)
        self.assertEqual(self.obj.atlas.contactInfoVisible, False)

    def test_signup_atlas_contact(self):
        self.submit_form('/portal/edit/atlas/', 'input_id_submit', select_checkboxes={
            'id_included': True,
            'id_birthdayVisible': False,
            'id_contactInfoVisible': True,
        })

        self.assertEqual(self.current_url, '/portal/edit/atlas/',
                         'Check that we stayed on the right page')

        self.assertEqual(self.obj.atlas.included, True)
        self.assertEqual(self.obj.atlas.birthdayVisible, False)
        self.assertEqual(self.obj.atlas.contactInfoVisible, True)

    def test_signup_atlas_minimal(self):
        self.submit_form('/portal/edit/atlas/', 'input_id_submit', select_checkboxes={
            'id_included': True,
            'id_birthdayVisible': False,
            'id_contactInfoVisible': False,
        })

        self.assertEqual(self.current_url, '/portal/edit/atlas/',
                         'Check that we stayed on the right page')

        self.assertEqual(self.obj.atlas.included, True)
        self.assertEqual(self.obj.atlas.birthdayVisible, False)
        self.assertEqual(self.obj.atlas.contactInfoVisible, False)

    def test_signup_atlas_empty(self):
        self.submit_form('/portal/edit/atlas/', 'input_id_submit', select_checkboxes={
            'id_included': False,
            'id_birthdayVisible': False,
            'id_contactInfoVisible': False,
        })

        self.assertEqual(self.current_url, '/portal/edit/atlas/',
                         'Check that we stayed on the right page')

        obj = Alumni.objects.first().atlas
        self.assertEqual(self.obj.atlas.included, False)
        self.assertEqual(self.obj.atlas.birthdayVisible, False)
        self.assertEqual(self.obj.atlas.contactInfoVisible, False)
