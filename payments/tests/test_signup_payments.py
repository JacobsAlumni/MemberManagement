from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.utils import timezone

from alumni.fields.tier import TierField
from MemberManagement.tests.integration import IntegrationTest
from payments.models import SubscriptionInformation

from .paymentmethod import PaymentMethodTest

MOCKED_TIME = timezone.datetime(
    2019, 9, 19, 16, 41, 17, 40, tzinfo=timezone.utc)

class SignupPaymentsTestMixin(PaymentMethodTest):
    def test_card_ok(self):
        self.load_live_url('setup_subscription', '#id_payment_type')
        self.assert_card_selectable()

    def test_iban_ok(self):
        self.load_live_url('setup_subscription', '#id_payment_type')
        self.assert_iban_selectable()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=('sub_fake', None))
    def test_signup_card_ok(self, cmock, umock):
        # fill out and submit card details
        self.load_live_url('setup_subscription', '#id_payment_type')
        self.submit_card_details()

        # check that things are as expected
        self.assert_url_equal('setup_setup',
                         'Check that the user gets redirected to the completed page')

        # check that the mocks were called
        umock.assert_has_calls([mock.call(self.user.alumni.membership.customer, "", "fake-token-id")])
        cmock.assert_has_calls([mock.call(self.user.alumni.membership.customer, self.__class__.subscribe_field_value)])

        # check that the subscription object was created
        subscription = self.user.alumni.subscription
        self.assertEqual(subscription.start, MOCKED_TIME)
        self.assertEqual(subscription.end, None)
        self.assertEqual(subscription.subscription, 'sub_fake')
        self.assertEqual(subscription.external, False)
        self.assertEqual(subscription.tier, self.user.alumni.membership.tier)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure')))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=('sub_fake', None))
    def test_signup_card_error_update_method(self, cmock, umock):
        # fill out and submit card details
        self.load_live_url('setup_subscription', '#id_payment_type')
        self.submit_card_details()

        # check that things are as expected
        self.assert_url_equal('setup_subscription',
                         'Check that the user stays on the first page')

        # check that only the first mock was called
        umock.assert_has_calls([mock.call(self.user.alumni.membership.customer, "", "fake-token-id")])
        cmock.assert_not_called()

        # check that the subscription object was not created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(
                member=self.user.alumni)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(None, Exception('Debug Error')))
    def test_signup_card_error_create_subscription(self, cmock, umock):
        # fill out and submit card details
        self.load_live_url('setup_subscription', '#id_payment_type')
        self.submit_card_details()

        # check that things are as expected
        self.assert_url_equal('setup_subscription',
                         'Check that the user stays on the subscribe page')

        # check that only the first mock was called
        umock.assert_has_calls([mock.call(self.user.alumni.membership.customer, "", "fake-token-id")])
        cmock.assert_has_calls([mock.call(self.user.alumni.membership.customer, self.__class__.subscribe_field_value)])

        # check that the subscription object was not created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(
                member=self.user.alumni)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=('sub_fake', None))
    def test_signup_sepa(self, cmock, umock):
        self.load_live_url('setup_subscription', '#id_payment_type')
        self.submit_sepa_details()

        # check that things are as expected
        self.assert_url_equal('setup_setup',
                         'Check that the user gets redirected to the completed page')

        # check that the mocks were called
        umock.assert_has_calls([mock.call(self.user.alumni.membership.customer, "fake-source-id", "")])
        cmock.assert_has_calls([mock.call(self.user.alumni.membership.customer, self.__class__.subscribe_field_value)])

        # check that the subscription object was created
        subscription = self.user.alumni.subscription
        self.assertEqual(subscription.start, MOCKED_TIME)
        self.assertEqual(subscription.end, None)
        self.assertEqual(subscription.subscription, 'sub_fake')
        self.assertEqual(subscription.external, False)
        self.assertEqual(subscription.tier, self.user.alumni.membership.tier)

    @mock.patch('django.utils.timezone.now',
                mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure')))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=('sub_fake', None))
    def test_signup_sepa_error_update_method(self, cmock, umock):
        # fill out and submit sepa details
        self.load_live_url('setup_subscription', '#id_payment_type')
        self.submit_sepa_details()

        # check that things are as expected
        self.assert_url_equal('setup_subscription',
                         'Check that the user stays on the first page')

        # check that only the first mock was called
        umock.assert_has_calls([mock.call(self.user.alumni.membership.customer, "fake-source-id", "")])
        cmock.assert_not_called()

        # check that the subscription object was not created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(
                member=self.user.alumni)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(None, Exception('Debug Error')))
    def test_signup_sepa_error_create_subscription(self, cmock, umock):
        # fill out and submit card details
        self.load_live_url('setup_subscription', '#id_payment_type')
        self.submit_sepa_details()

        # check that things are as expected
        self.assert_url_equal('setup_subscription',
                         'Check that the user stays on the subscribe page')

        # check that only the first mock was called
        umock.assert_has_calls([mock.call(self.user.alumni.membership.customer, "fake-source-id", "")])
        cmock.assert_has_calls([mock.call(self.user.alumni.membership.customer, self.__class__.subscribe_field_value)])

        # check that the subscription object was not created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(
                member=self.user.alumni)


class ContributorSubscribeTest(SignupPaymentsTestMixin, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_07b_contributor.json']
    user = 'Mounfem'
    subscribe_field_value = 'contributor-membership'


class PatronSubscribeTest(SignupPaymentsTestMixin, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_07c_patron.json']
    user = 'Mounfem'
    subscribe_field_value = 'patron-membership'
