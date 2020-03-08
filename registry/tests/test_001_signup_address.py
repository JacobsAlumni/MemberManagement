from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest

class AddressTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_00_register.json']
    user = 'Mounfem'

    def test_signup_address_minimal(self):
        self.submit_form('setup_address', 'input_id_submit', send_form_keys={
            'id_address_line_1': 'Alt-Moabit 72',
            'id_address_line_2': '',
            'id_city': 'Breunsdorf',
            'id_zip': '04574',
            'id_state': ''
        }, select_dropdowns={
            'id_country': ('DE',)
        })

        self.assert_url_equal('setup_social',
                              'Check that the user gets redirected to the social page')

        address = self.user.alumni.address
        self.assertEqual(address.address_line_1, 'Alt-Moabit 72')
        self.assertEqual(address.address_line_2, None)
        self.assertEqual(address.city, 'Breunsdorf')
        self.assertEqual(address.zip, '04574')
        self.assertEqual(address.state, None)
        self.assertEqual(address.country.name, 'Germany')

    def test_signup_address_full(self):
        self.submit_form('setup_address', 'input_id_submit', send_form_keys={
            'id_address_line_1': '2986 Heron Way',
            'id_address_line_2': 'Attn. Anna Freytag',
            'id_city': 'Portland',
            'id_zip': '97205',
            'id_state': 'Oregon'
        }, select_dropdowns={
            'id_country': ('US',)
        })

        self.assert_url_equal('setup_social',
                              'Check that the user gets redirected to the social page')

        address = self.user.alumni.address
        self.assertEqual(address.address_line_1, '2986 Heron Way')
        self.assertEqual(address.address_line_2, 'Attn. Anna Freytag')
        self.assertEqual(address.city, 'Portland')
        self.assertEqual(address.zip, '97205')
        self.assertEqual(address.state, 'Oregon')
        self.assertEqual(address.country.name, 'United States of America')

    def test_signup_address_fail(self):
        button = self.fill_out_form(
            'setup_address', 'input_id_submit')

        # remove all the 'required' elements
        self.disable_form_requirements()

        # then click the button and wait
        button.click()
        self.find_element('.main-container')

        # check that we didn't get redirected
        self.assert_url_equal('setup_address',
                              'Check that the user stays on the address page')

        for id_ in ['id_address_line_1', 'id_zip', 'id_city', 'id_country']:
            self.assertIn('uk-form-danger', self.selenium.find_element_by_id(id_).get_attribute(
                'class').split(' '), '{} field marked up as incorrect'.format(id_))
