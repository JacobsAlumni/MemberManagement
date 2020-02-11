from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest


class EditAddressTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')
        self.obj = Alumni.objects.get(profile__username='Mounfem')

    def test_noedit(self):
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('/portal/edit/address/', 'input_id_submit')

        # check that nothing happened
        self.assertEqual(self.current_url, '/portal/edit/address/',
                         'Check that we stayed on the right page')

        # check that everything stayed the same
        self.assertEqual(self.obj.address.address_line_1, 'Alt-Moabit 72')
        self.assertEqual(self.obj.address.address_line_2, None)
        self.assertEqual(self.obj.address.city, 'Breunsdorf')
        self.assertEqual(self.obj.address.zip, '04574')
        self.assertEqual(self.obj.address.state, 'Sachsen')
        self.assertEqual(self.obj.address.country.name, 'Germany')

    def test_edit_full(self):
        """ Tests that adding a full address works """

        # enter nothing
        self.submit_form('/portal/edit/address/', 'input_id_submit', send_form_keys={
            'id_address_line_1': '2986 Heron Way',
            'id_address_line_2': 'Attn. Anna Freytag',
            'id_city': 'Portland',
            'id_zip': '97205',
            'id_state': 'Oregon'
        }, select_dropdowns={
            'id_country': ('US',)
        })

        # check that nothing happened
        self.assertEqual(self.current_url, '/portal/edit/address/',
                         'Check that we stayed on the right page')

        # check that we edited it right
        self.assertEqual(self.obj.address.address_line_1, '2986 Heron Way')
        self.assertEqual(self.obj.address.address_line_2, 'Attn. Anna Freytag')
        self.assertEqual(self.obj.address.city, 'Portland')
        self.assertEqual(self.obj.address.zip, '97205')
        self.assertEqual(self.obj.address.state, 'Oregon')
        self.assertEqual(self.obj.address.country.name,
                         'United States of America')

    def test_edit_noempty(self):
        """ Tests that adding a full address works """

        # enter nothing
        button = self.fill_out_form('/portal/edit/address/', 'input_id_submit', send_form_keys={
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
        self.wait_for_element('.main-container')

        # check that nothing happened
        self.assertEqual(self.current_url, '/portal/edit/address/',
                         'Check that we stayed on the right page')

        # check that nothing was edited
        self.assertEqual(self.obj.address.address_line_1, 'Alt-Moabit 72')
        self.assertEqual(self.obj.address.address_line_2, None)
        self.assertEqual(self.obj.address.city, 'Breunsdorf')
        self.assertEqual(self.obj.address.zip, '04574')
        self.assertEqual(self.obj.address.state, 'Sachsen')
        self.assertEqual(self.obj.address.country.name, 'Germany')

        # and fields were marked as incorrect
        for id_ in ['id_address_line_1', 'id_zip', 'id_city']:
            self.assertIn('uk-form-danger', self.selenium.find_element_by_id(id_).get_attribute(
                'class').split(' '), '{} field marked up as incorrect'.format(id_))
