from __future__ import annotations

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from MemberManagement.tests.integration import IntegrationTest

from selenium.webdriver.common.by import By


class EditAddressTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Mounfem'

    def test_noedit(self) -> None:
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('edit_address', 'input_id_submit')
        self.assert_url_equal('edit_address')

        # check that everything stayed the same
        address = self.user.alumni.address
        self.assertEqual(address.address_line_1, 'Alt-Moabit 72')
        self.assertEqual(address.address_line_2, None)
        self.assertEqual(address.city, 'Breunsdorf')
        self.assertEqual(address.zip, '04574')
        self.assertEqual(address.state, 'Sachsen')
        self.assertEqual(address.country.name, 'Germany')

    def test_edit_full(self) -> None:
        """ Tests that adding a full address works """

        # enter nothing
        self.submit_form('edit_address', 'input_id_submit', send_form_keys={
            'id_address_line_1': '2986 Heron Way',
            'id_address_line_2': 'Attn. Anna Freytag',
            'id_city': 'Portland',
            'id_zip': '97205',
            'id_state': 'Oregon'
        }, select_dropdowns={
            'id_country': ('US',)
        })

        # check that nothing happened
        self.assert_url_equal('edit_address',
                              'Check that we stayed on the right page')

        # check that we edited it right
        address = self.user.alumni.address
        self.assertEqual(address.address_line_1, '2986 Heron Way')
        self.assertEqual(address.address_line_2, 'Attn. Anna Freytag')
        self.assertEqual(address.city, 'Portland')
        self.assertEqual(address.zip, '97205')
        self.assertEqual(address.state, 'Oregon')
        self.assertEqual(address.country.name,
                         'United States of America')

    def test_edit_noempty(self) -> None:
        """ Tests that adding a full address works """

        # enter nothing
        button = self.fill_out_form('edit_address', 'input_id_submit', send_form_keys={
            'id_address_line_1': '',
            'id_address_line_2': '',
            'id_city': '',
            'id_zip': '',
            'id_state': ''
        }, select_dropdowns={
            'id_country': (),
        })

        self.disable_form_requirements()

        button.click()
        self.find_element('.main-container')

        # check that nothing happened
        self.assert_url_equal('edit_address',
                              'Check that we stayed on the right page')

        # check that nothing was edited
        address = self.user.alumni.address
        self.assertEqual(address.address_line_1, 'Alt-Moabit 72')
        self.assertEqual(address.address_line_2, None)
        self.assertEqual(address.city, 'Breunsdorf')
        self.assertEqual(address.zip, '04574')
        self.assertEqual(address.state, 'Sachsen')
        self.assertEqual(address.country.name, 'Germany')

        # and fields were marked as incorrect
        for id_ in ['id_address_line_1', 'id_zip', 'id_city']:
            self.assertIn('uk-form-danger', self.selenium.find_element(By.ID, id_).get_attribute(
                'class').split(' '), '{} field marked up as incorrect'.format(id_))
