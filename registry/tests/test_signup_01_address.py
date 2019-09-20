from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest

from alumni.models import Alumni


class AddressTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_00_register.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')

    def test_signup_address_minimal(self):
        self.submit_form('/portal/setup/address/', 'input_id_submit', send_form_keys={
            'id_address_line_1': 'Alt-Moabit 72',
            'id_address_line_2': '',
            'id_city': 'Breunsdorf',
            'id_zip': '04574',
            'id_state': ''
        }, select_dropdowns={
            'id_country': ('DE',)
        })

        self.assertEqual(self.current_url, '/portal/setup/social/',
                         'Check that the user gets redirected to the social page')

        obj = Alumni.objects.first().address
        self.assertEqual(obj.address_line_1, 'Alt-Moabit 72')
        self.assertEqual(obj.address_line_2, None)
        self.assertEqual(obj.city, 'Breunsdorf')
        self.assertEqual(obj.zip, '04574')
        self.assertEqual(obj.state, None)
        self.assertEqual(obj.country.name, 'Germany')

    def test_signup_address_full(self):
        self.submit_form('/portal/setup/address/', 'input_id_submit', send_form_keys={
            'id_address_line_1': '2986 Heron Way',
            'id_address_line_2': 'Attn. Anna Freytag',
            'id_city': 'Portland',
            'id_zip': '97205',
            'id_state': 'Oregon'
        }, select_dropdowns={
            'id_country': ('US',)
        })

        self.assertEqual(self.current_url, '/portal/setup/social/',
                         'Check that the user gets redirected to the social page')

        obj = Alumni.objects.first().address
        self.assertEqual(obj.address_line_1, '2986 Heron Way')
        self.assertEqual(obj.address_line_2, 'Attn. Anna Freytag')
        self.assertEqual(obj.city, 'Portland')
        self.assertEqual(obj.zip, '97205')
        self.assertEqual(obj.state, 'Oregon')
        self.assertEqual(obj.country.name, 'United States of America')

    def test_signup_address_fail(self):
        button = self.fill_out_form(
            '/portal/setup/address/', 'input_id_submit')

        # remove all the 'required' elements
        self.selenium.execute_script("""
        var inputs = document.getElementsByTagName('input');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].removeAttribute('required');
        }
        var selects = document.getElementsByTagName('select');
        for (var i = 0; i < selects.length; i++) {
            selects[i].removeAttribute('required');
        }
        """)

        # then click the button and wait
        button.click()
        self.wait_for_element('body')

        # check that we didn't get redirected
        self.assertEqual(self.current_url, '/portal/setup/address/',
                         'Check that the user stays on the address page')

        for id_ in ['id_address_line_1', 'id_zip', 'id_city', 'id_country']:
            self.assertIn('uk-form-danger', self.selenium.find_element_by_id(id_).get_attribute(
                'class').split(' '), '{} field marked up as incorrect'.format(id_))
