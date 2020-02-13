from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from MemberManagement.tests.integration import IntegrationTest

from unittest import mock

from alumni.models import Alumni
from alumni.fields.tier import TierField

from payments.models import SubscriptionInformation, MembershipInformation

MOCKED_CUSTOMER = mock.MagicMock(id='cus_Fq8yG7rLrc6sKZ')


class PatronTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_06_atlas.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')

    def test_setup_patron_elements(self):
        # fill out the form and select the patron tier
        self.fill_out_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": 'Patron – Premium membership for 249€ p.a.'
        })

        self.assertFalse(self.selenium.find_element_by_id(
            'description-st').is_displayed())
        self.assertFalse(self.selenium.find_element_by_id(
            'description-co').is_displayed())
        self.assertTrue(self.selenium.find_element_by_id(
            'description-pa').is_displayed())

    def test_setup_patron(self):
        with mock.patch('payments.stripewrapper.create_customer', return_value=(MOCKED_CUSTOMER, None)) as mocked:
            # fill out the form an select the patron tier
            self.submit_form('setup_membership', 'input_id_submit', select_dropdowns={
                "id_tier": 'Patron – Premium membership for 249€ p.a.'
            })

            self.assertEqual(self.current_url, reverse('setup_subscription'),
                             'Check that the user gets redirected to the subscription page')

            # check that the stripe api was called with the object as a parameter
            obj = Alumni.objects.first()
            self.assertListEqual(mocked.call_args_list, [mock.call(obj)])

            # check that the membership object was created
            obj = Alumni.objects.first().membership
            self.assertEqual(obj.tier, TierField.PATRON)
            self.assertEqual(obj.customer, 'cus_Fq8yG7rLrc6sKZ')

            # Check that the subscription object was *not* created
            with self.assertRaises(SubscriptionInformation.DoesNotExist):
                SubscriptionInformation.objects.get(
                    member=Alumni.objects.first())

    def test_setup_patron_fail(self):
        with mock.patch('payments.stripewrapper.create_customer', return_value=(None, "debug")) as mocked:
            # fill out the form an select the payments tier
            self.submit_form('setup_membership', 'input_id_submit', select_dropdowns={
                "id_tier": 'Patron – Premium membership for 249€ p.a.'
            })

            # we stay on the same page
            self.assertEqual(self.current_url, reverse('setup_membership'),
                             'Check that the user does not get redirected to the final page')

            # check that the stripe api was called with the object as a parameter
            obj = Alumni.objects.first()
            self.assertListEqual(mocked.call_args_list, [mock.call(obj)])

            # Check that the membership object was *not* created
            with self.assertRaises(MembershipInformation.DoesNotExist):
                Alumni.objects.first().membership

            # Check that the subscription object was *not* created
            with self.assertRaises(SubscriptionInformation.DoesNotExist):
                SubscriptionInformation.objects.get(
                    member=Alumni.objects.first())
