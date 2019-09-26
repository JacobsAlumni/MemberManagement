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
MOCKED_STARTER_CUSTOMER = mock.MagicMock(id='cus_Fq8yG7rLrc6sKZ')


class StarterTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_06_atlas.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_setup_starter(self):
        with mock.patch('payments.stripewrapper.create_customer', return_value=(MOCKED_STARTER_CUSTOMER, None)) as mocked:
            # fill out the form an select the starter tier
            btn = self.fill_out_form('/payments/membership/', 'input_id_submit', select_dropdowns={
                "id_tier": 'Starter (If graduated less than 2 years ago or not ready to financially contribute): free'
            })

            # enter a reason
            self.selenium.find_element_by_id(
                'id_starterReason').send_keys('Because I am testing')

            # click the submit button and wait for the page to load
            btn.click()
            self.wait_for_element(None)

            self.assertEqual(self.current_url, '/portal/setup/completed/',
                             'Check that the user gets redirected to the final page')

            # check that the stripe api was called with the object as a parameter
            obj = Alumni.objects.first()
            self.assertListEqual(mocked.call_args_list, [mock.call(obj)])

            # check that the membership object was created
            obj = Alumni.objects.first().membership
            self.assertEqual(obj.tier, TierField.STARTER)
            self.assertEqual(obj.starterReason, 'Because I am testing')
            self.assertEqual(obj.customer, 'cus_Fq8yG7rLrc6sKZ')

            # check that the subscription was created appropriately
            obj = SubscriptionInformation.objects.get(
                member=Alumni.objects.first())
            self.assertEqual(obj.start, MOCKED_TIME)
            self.assertEqual(obj.end, MOCKED_TIME + timedelta(days=2 * 365))
            self.assertEqual(obj.subscription, None)
            self.assertEqual(obj.external, False)
            self.assertEqual(obj.tier, TierField.STARTER)

    def test_setup_starter_fail(self):
        with mock.patch('payments.stripewrapper.create_customer', return_value=(None, "debug")) as mocked:
            # fill out the form an select the starter tier
            btn = self.fill_out_form('/payments/membership/', 'input_id_submit', select_dropdowns={
                "id_tier": 'Starter (If graduated less than 2 years ago or not ready to financially contribute): free'
            })

            # enter a reason
            self.selenium.find_element_by_id(
                'id_starterReason').send_keys('Because I am testing')

            # click the submit button and wait for the page to load
            btn.click()
            self.wait_for_element(None)

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
