from datetime import timedelta
from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone

from alumni.fields.tier import TierField
from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest
from payments.models import MembershipInformation, SubscriptionInformation

MOCKED_TIME = timezone.datetime(
    2019, 9, 19, 16, 41, 17, 40, tzinfo=timezone.utc)
MOCKED_END = MOCKED_TIME + timedelta(days=2 * 365)
MOCKED_CUSTOMER = mock.MagicMock(id='cus_Fq8yG7rLrc6sKZ')


class StarterTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_06_atlas.json']
    user = 'Mounfem'

    def test_setup_starter_elements(self):
        # fill out the form and select the starter tier
        self.fill_out_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": 'Starter – Free Membership for 0€ p.a.'
        })

        self.assert_element_displayed('#description-st')
        self.assert_element_not_displayed('#description-co')
        self.assert_element_not_displayed('#description-pa')

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.create_customer', return_value=(MOCKED_CUSTOMER, None))
    def test_setup_starter(self, mocked):
        self.submit_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": 'Starter – Free Membership for 0€ p.a.'
        })

        self.assert_url_equal('setup_setup',
                              'Check that the user gets redirected to the final page')

        # check that the stripe api was called with the object as a parameter
        alumni = self.user.alumni
        mocked.assert_has_calls([mock.call(alumni)])

        # check that the membership object was created
        membership = alumni.membership
        self.assertEqual(membership.tier, TierField.STARTER)
        self.assertEqual(membership.customer, 'cus_Fq8yG7rLrc6sKZ')

        # check that the subscription was created appropriately
        subscription = SubscriptionInformation.objects.get(member=alumni)
        self.assertEqual(subscription.start, MOCKED_TIME)
        self.assertEqual(subscription.end, MOCKED_END)
        self.assertEqual(subscription.subscription, None)
        self.assertEqual(subscription.external, False)
        self.assertEqual(subscription.tier, TierField.STARTER)

    @mock.patch('payments.stripewrapper.create_customer', return_value=(None, "debug"))
    def test_setup_starter_fail(self, mocked):
        # fill out the form an select the starter tier
        btn = self.fill_out_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": 'Starter – Free Membership for 0€ p.a.'
        })

        # click the submit button and wait for the page to load
        btn.click()
        self.find_element(None)

        # we stay on the same page
        self.assert_url_equal('setup_membership',
                              'Check that the user does not get redirected to the final page')

        # check that the stripe api was called with the object as a parameter
        alumni = self.user.alumni
        mocked.assert_has_calls([mock.call(alumni)])

        # Check that the membership object was *not* created
        with self.assertRaises(MembershipInformation.DoesNotExist):
            alumni.membership

        # Check that the subscription object was *not* created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(member=alumni)
