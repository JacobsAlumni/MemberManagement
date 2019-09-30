from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest

from django.utils import timezone
from datetime import timedelta

from unittest import mock

from alumni.models import Alumni
from alumni.fields.tier import TierField

from payments.models import SubscriptionInformation, MembershipInformation

MOCKED_TIME = timezone.datetime(
    2019, 9, 19, 16, 41, 17, 40, tzinfo=timezone.utc)
MOCKED_CUSTOMER = mock.MagicMock(id='cus_Fq8yG7rLrc6sKZ')


class ContributorTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_06_atlas.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')
    
    def test_setup_contributor_elements(self):
        # fill out the form and select the contributor tier
        self.fill_out_form('/payments/membership/', 'input_id_submit', select_dropdowns={
            "id_tier": 'Contributor (Standard package if graduated more than 2 years ago): 39€ p.a.'
        })

        self.assertFalse(self.selenium.find_element_by_id('id_starterReason').is_displayed())
        self.assertFalse(self.selenium.find_element_by_id('description-st').is_displayed())
        self.assertTrue(self.selenium.find_element_by_id('description-co').is_displayed())
        self.assertFalse(self.selenium.find_element_by_id('description-pa').is_displayed())

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_setup_contributor(self):
        with mock.patch('payments.stripewrapper.create_customer', return_value=(MOCKED_CUSTOMER, None)) as mocked:
            # fill out the form an select the contributor tier
            self.submit_form('/payments/membership/', 'input_id_submit', select_dropdowns={
                "id_tier": 'Contributor (Standard package if graduated more than 2 years ago): 39€ p.a.'
            })

            self.assertEqual(self.current_url, '/payments/subscribe/',
                             'Check that the user gets redirected to the subscription page')

            # check that the stripe api was called with the object as a parameter
            obj = Alumni.objects.first()
            self.assertListEqual(mocked.call_args_list, [mock.call(obj)])

            # check that the membership object was created
            obj = Alumni.objects.first().membership
            self.assertEqual(obj.tier, TierField.CONTRIBUTOR)
            self.assertEqual(obj.starterReason, '')
            self.assertEqual(obj.customer, 'cus_Fq8yG7rLrc6sKZ')

            # Check that the subscription object was *not* created
            with self.assertRaises(SubscriptionInformation.DoesNotExist):
                SubscriptionInformation.objects.get(
                    member=Alumni.objects.first())

    def test_setup_contributor_fail(self):
        with mock.patch('payments.stripewrapper.create_customer', return_value=(None, "debug")) as mocked:
            # fill out the form an select the payments tier
            self.submit_form('/payments/membership/', 'input_id_submit', select_dropdowns={
                "id_tier": 'Contributor (Standard package if graduated more than 2 years ago): 39€ p.a.'
            })

            # we stay on the same page
            self.assertEqual(self.current_url, '/payments/membership/',
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
