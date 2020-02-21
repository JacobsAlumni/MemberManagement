import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from alumni.fields.category import AlumniCategoryField
from alumni.fields.gender import GenderField
from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest


class SignupTest(IntegrationTest, StaticLiveServerTestCase):
    def test_signup_regular(self):
        """ Tests that we can complete the first setup page with a regular user """

        # fill out a new form on the register page
        self.submit_form('register', 'input_id_submit', send_form_keys={
            'id_givenName': 'Anna',
            'id_middleName': '',
            'id_familyName': 'Freytag',
            'id_email': 'AnnaFreytag@dayrep.com',
            'id_username': 'Mounfem',
        }, select_dropdowns={
            'id_sex': 'Female',
            'id_nationality': ('DE',),
            'id_category': (AlumniCategoryField.REGULAR,)
        }, select_checkboxes={
            'id_resetExistingEmailPassword': False,
            'id_tos': True
        }, script_value={
            'id_birthday': '1948-11-07',
        })

        # check that we got redirected to the right url
        self.assert_url_equal('setup_address',
                              'Check that the user gets redirected to the second page')

        # check that the right alumni object was created
        obj = Alumni.objects.first()
        self.assertEqual(obj.profile.username, 'Mounfem')
        self.assertEqual(obj.givenName, 'Anna')
        self.assertEqual(obj.middleName, None)
        self.assertEqual(obj.familyName, 'Freytag')
        self.assertEqual(obj.email, 'AnnaFreytag@dayrep.com')
        self.assertEqual(obj.existingEmail, None)
        self.assertEqual(obj.resetExistingEmailPassword, False)
        self.assertEqual(obj.sex, GenderField.FEMALE)
        self.assertEqual(obj.birthday, datetime.date(1948, 11, 7))
        self.assertListEqual(
            list(map(lambda c: c.name, obj.nationality)), ['Germany'])
        self.assertEqual(obj.category, AlumniCategoryField.REGULAR)

        # check that the approval object is created
        obj = Alumni.objects.first().approval
        self.assertEqual(obj.approval, False)
        self.assertEqual(obj.gsuite, None)
        self.assertEqual(obj.time, None)

    def test_signup_faculty(self):
        """ Tests that we can complete the first signup page for a faculty member """

        # fill out a new form on the register page
        self.submit_form('register', 'input_id_submit', send_form_keys={
            'id_givenName': 'David',
            'id_middleName': 'L',
            'id_familyName': 'Hood',
            'id_existingEmail': 'dhood@jacobs-alumni.de',
            'id_email': 'DavidLHood@armyspy.com',
            'id_username': 'Heak1991',
        }, select_dropdowns={
            'id_sex': 'Male',
            'id_nationality': ('US',),
            'id_category': (AlumniCategoryField.FACULTY,)
        }, select_checkboxes={
            'id_resetExistingEmailPassword': True,
            'id_tos': True
        }, script_value={
            'id_birthday': '1991-04-09',
        })

        # check that we got redirected to the right url
        self.assert_url_equal('setup_address',
                              'Check that the user gets redirected to the second page')

        # check that the right alumni object was created
        obj = Alumni.objects.first()
        self.assertEqual(obj.profile.username, 'Heak1991')
        self.assertEqual(obj.givenName, 'David')
        self.assertEqual(obj.middleName, 'L')
        self.assertEqual(obj.familyName, 'Hood')
        self.assertEqual(obj.email, 'DavidLHood@armyspy.com')
        self.assertEqual(obj.existingEmail, 'dhood@jacobs-alumni.de')
        self.assertEqual(obj.resetExistingEmailPassword, True)
        self.assertEqual(obj.sex, GenderField.MALE)
        self.assertEqual(obj.birthday, datetime.date(1991, 4, 9))
        self.assertListEqual(list(map(lambda c: c.name, obj.nationality)), [
                             'United States of America'])
        self.assertEqual(obj.category, AlumniCategoryField.FACULTY)

        # check that the approval object is created
        obj = Alumni.objects.first().approval
        self.assertEqual(obj.approval, False)
        self.assertEqual(obj.gsuite, None)
        self.assertEqual(obj.time, None)

    def test_signup_notos(self):
        """ Tests that we can not submit a form without having accepted the TOS """

        # fill out the form first
        button = self.fill_out_form('register', 'input_id_submit', send_form_keys={
            'id_givenName': 'Anna',
            'id_middleName': '',
            'id_familyName': 'Freytag',
            'id_email': 'AnnaFreytag@dayrep.com',
            'id_username': 'Mounfem',
        }, select_dropdowns={
            'id_sex': 'Female',
            'id_nationality': ('DE',),
            'id_category': (AlumniCategoryField.REGULAR,)
        }, select_checkboxes={
            'id_resetExistingEmailPassword': False,
            'id_tos': False
        }, script_value={
            'id_birthday': '1948-11-07',
        })

        # assume the user did some clever inspect element magic
        self.selenium.execute_script(
            'arguments[0].removeAttribute("required")', self.selenium.find_element_by_id('id_tos'))

        # then click the button and wait
        button.click()
        self.find_element('.main-container')

        # check that we didn't get redirected
        self.assert_url_equal('register',
                              'Check that the user stays on the first page')
        self.assertIn('uk-form-danger', self.selenium.find_element_by_id(
            'id_tos').get_attribute('class').split(' '), 'tos field marked up as incorrect')

    def test_signup_alumniemail(self):
        """ Tests that we can not complete the first setup page with a jacobs alumni email """

        self.submit_form('register', 'input_id_submit', send_form_keys={
            'id_givenName': 'David',
            'id_middleName': 'L',
            'id_familyName': 'Hood',
            'id_existingEmail': 'dhood@jacobs-alumni.de',
            'id_email': 'dhood@jacobs-alumni.de',
            'id_username': 'Heak1991',
        }, select_dropdowns={
            'id_sex': 'Male',
            'id_nationality': ('US',),
            'id_category': (AlumniCategoryField.FACULTY,)
        }, select_checkboxes={
            'id_resetExistingEmailPassword': True,
            'id_tos': True
        }, script_value={
            'id_birthday': '1991-04-09',
        })

        self.assert_url_equal('register',
                              'Check that the user stays on the first page')
        self.assertIn('uk-form-danger', self.selenium.find_element_by_id(
            'id_email').get_attribute('class').split(' '), 'email field marked up as incorrect')

    def test_signup_jacobsemail(self):
        """ Tests that we can not complete the first setup page with a jacobs alumni email """

        self.submit_form('register', 'input_id_submit', send_form_keys={
            'id_givenName': 'David',
            'id_middleName': 'L',
            'id_familyName': 'Hood',
            'id_existingEmail': 'dhood@jacobs-alumni.de',
            'id_email': 'dhood@jacobs-university.de',
            'id_username': 'Heak1991',
        }, select_dropdowns={
            'id_sex': 'Male',
            'id_nationality': ('US',),
            'id_category': (AlumniCategoryField.FACULTY,)
        }, select_checkboxes={
            'id_resetExistingEmailPassword': True,
            'id_tos': True
        }, script_value={
            'id_birthday': '1991-04-09',
        })

        self.assert_url_equal(
            'register', 'Check that the user stays on the first page')
        self.assertIn('uk-form-danger', self.selenium.find_element_by_id(
            'id_email').get_attribute('class').split(' '), 'email field marked up as incorrect')
