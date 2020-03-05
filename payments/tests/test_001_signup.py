from datetime import timedelta
from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone

from alumni.fields.tier import TierField
from MemberManagement.tests.integration import IntegrationTest, IntegrationTestBase
from payments.models import MembershipInformation, SubscriptionInformation

MOCKED_TIME = timezone.datetime(
    2019, 9, 19, 16, 41, 17, 40, tzinfo=timezone.utc)
MOCKED_END = MOCKED_TIME + timedelta(days=2 * 365)
MOCKED_CUSTOMER = 'cus_Fq8yG7rLrc6sKZ'


class SignupTestBase(IntegrationTestBase):
    def test_setup_tier_elements(self):
        # fill out the tier and check that the right tier into is displayed
        self.fill_out_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(self.__class__.tier)
        })

        for tier in [TierField.STARTER, TierField.CONTRIBUTOR, TierField.PATRON]:
            if tier == self.__class__.tier:
                self.assert_element_displayed('#description-{}'.format(tier))
            else:
                self.assert_element_not_displayed(
                    '#description-{}'.format(tier))

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.create_customer', return_value=(MOCKED_CUSTOMER, None))
    def test_setup_tier_ok(self, mocked):
        # fill out the form an select the contributor tier
        self.submit_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(self.__class__.tier)
        })

        self.assert_url_equal('setup_subscription',
                              'Check that the user gets redirected to the subscription page')

        # check that the stripe api was called with the object as a parameter
        alumni = self.user.alumni
        mocked.assert_has_calls([mock.call(alumni)])

        # check that the membership object was created
        membership = alumni.membership
        self.assertEqual(membership.tier, self.__class__.tier)
        self.assertEqual(membership.customer, MOCKED_CUSTOMER)

        # Check that the subscription object was *not* created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(member=alumni)

    @mock.patch('payments.stripewrapper.create_customer', return_value=(None, "debug"))
    def test_setup_tier_fail(self, mocked):
        # fill out the form an select the starter tier
        btn = self.fill_out_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(self.__class__.tier)
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


class StarterSignupTest(SignupTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_06_atlas.json']
    user = 'Mounfem'
    tier = TierField.STARTER

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.create_customer', return_value=(MOCKED_CUSTOMER, None))
    def test_setup_tier_ok(self, mocked):
        self.submit_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(TierField.STARTER)
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


class ContributorSignupTest(SignupTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_06_atlas.json']
    user = 'Mounfem'
    tier = TierField.CONTRIBUTOR


class PatronSignupTest(SignupTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_06_atlas.json']
    user = 'Mounfem'
    tier = TierField.PATRON
