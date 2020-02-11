from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from alumni.fields.category import AlumniCategoryField
from alumni.fields.gender import GenderField
from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest

import datetime


class EditDataTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')
        self.obj = Alumni.objects.get(profile__username='Mounfem')

    def test_noedit(self):
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('/portal/edit/', 'input_id_submit')

        # check that nothing happened
        self.assertEqual(self.current_url, '/portal/edit/',
                         'Check that we stayed on the right page')

        # check that everything stayed the same
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.profile.username, 'Mounfem')
        self.assertEqual(self.obj.givenName, 'Anna')
        self.assertEqual(self.obj.middleName, None)
        self.assertEqual(self.obj.familyName, 'Freytag')
        self.assertEqual(self.obj.email, 'AnnaFreytag@dayrep.com')
        self.assertEqual(self.obj.existingEmail, None)
        self.assertEqual(self.obj.resetExistingEmailPassword, False)
        self.assertEqual(self.obj.sex, GenderField.FEMALE)
        self.assertEqual(self.obj.birthday, datetime.date(1948, 11, 7))
        self.assertListEqual(
            list(map(lambda c: c.name, self.obj.nationality)), ['Germany'])
        self.assertEqual(self.obj.category, AlumniCategoryField.REGULAR)

    def test_data_regular(self):
        """ Tests that all fields can be changed """

        self.submit_form('/portal/edit/', 'input_id_submit', send_form_keys={
            'id_givenName': 'John',
            'id_middleName': 'C',
            'id_familyName': 'Day',
            'id_email': 'JohnDay@dayrep.com',
        }, select_dropdowns={
            'id_sex': 'Male',
            'id_nationality': ('GM',),
            'id_category': (AlumniCategoryField.REGULAR,)
        }, script_value={
            'id_birthday': '1949-10-08',
        })

        # check that we got redirected to the right url
        self.assertEqual(self.current_url, '/portal/edit/',
                         'Check that we stayed on the right page')

        # check that the right alumni object was created
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.givenName, 'John')
        self.assertEqual(self.obj.middleName, 'C')
        self.assertEqual(self.obj.familyName, 'Day')
        self.assertEqual(self.obj.email, 'JohnDay@dayrep.com')
        self.assertEqual(self.obj.existingEmail, None)
        self.assertEqual(self.obj.resetExistingEmailPassword, False)
        self.assertEqual(self.obj.sex, GenderField.MALE)
        self.assertEqual(self.obj.birthday, datetime.date(1949, 10, 8))
        self.assertListEqual(
            list(map(lambda c: c.name, self.obj.nationality)), ['Gambia'])
        self.assertEqual(self.obj.category, AlumniCategoryField.REGULAR)

    def test_nojacobsemail(self):
        """ Tests that we can't use a jacobs email as private email """

        # enter nothing
        self.submit_form('/portal/edit/', 'input_id_submit', send_form_keys={
            'id_email': 'AnnaFreytag@jacobs-university.de',
        })

        # check that we stayed on the page, but the email field was marked incorrect
        self.assertEqual(self.current_url, '/portal/edit/',
                         'Check that we stayed on the right page')
        self.assertIn('uk-form-danger', self.selenium.find_element_by_id(
            'id_email').get_attribute('class').split(' '), 'email field marked up as incorrect')

        # check that everything stayed the same
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.profile.username, 'Mounfem')
        self.assertEqual(self.obj.givenName, 'Anna')
        self.assertEqual(self.obj.middleName, None)
        self.assertEqual(self.obj.familyName, 'Freytag')
        self.assertEqual(self.obj.email, 'AnnaFreytag@dayrep.com')
        self.assertEqual(self.obj.existingEmail, None)
        self.assertEqual(self.obj.resetExistingEmailPassword, False)
        self.assertEqual(self.obj.sex, GenderField.FEMALE)
        self.assertEqual(self.obj.birthday, datetime.date(1948, 11, 7))
        self.assertListEqual(
            list(map(lambda c: c.name, self.obj.nationality)), ['Germany'])
        self.assertEqual(self.obj.category, AlumniCategoryField.REGULAR)
