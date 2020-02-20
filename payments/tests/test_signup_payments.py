from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.utils import timezone

from alumni.fields.tier import TierField
from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest
from payments.models import SubscriptionInformation

from .paymentmethod import PaymentMethodTest

MOCKED_TIME = timezone.datetime(
    2019, 9, 19, 16, 41, 17, 40, tzinfo=timezone.utc)
MOCKED_SUBSCRIPTION = mock.MagicMock(id='sub_fake')


class SignupPaymentsTestMixin(PaymentMethodTest):
    def test_card_ok(self):
        self.sget('setup_subscription', '#id_payment_type')
        self.assert_card_selectable()

    def test_iban_ok(self):
        self.sget('setup_subscription', '#id_payment_type')
        self.assert_iban_selectable()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(MOCKED_SUBSCRIPTION, None))
    def test_signup_card_ok(self, cmock, umock):
        # fill out and submit card details
        self.sget('setup_subscription', '#id_payment_type')
        self.submit_card_details()

        # check that things are as expected
        self.assertEqual(self.current_url, reverse('setup_setup'),
                         'Check that the user gets redirected to the completed page')

        # check that the mocks were called
        self.assertListEqual(umock.call_args_list, [mock.call(
            self.customer_id, "", "fake-token-id")])
        self.assertListEqual(cmock.call_args_list, [mock.call(
            self.customer_id, self.subscribe_field_value)])

        # check that the subscription object was created
        obj = SubscriptionInformation.objects.get(
            member=Alumni.objects.first())
        self.assertEqual(obj.start, MOCKED_TIME)
        self.assertEqual(obj.end, None)
        self.assertEqual(obj.subscription, 'sub_fake')
        self.assertEqual(obj.external, False)
        self.assertEqual(obj.tier, self.tier_field_value)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure')))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(MOCKED_SUBSCRIPTION, None))
    def test_signup_card_error_update_method(self, cmock, umock):
        # fill out and submit card details
        self.sget('setup_subscription', '#id_payment_type')
        self.submit_card_details()

        # check that things are as expected
        self.assertEqual(self.current_url, reverse('setup_subscription'),
                         'Check that the user stays on the first page')

        # check that only the first mock was called
        self.assertListEqual(umock.call_args_list, [mock.call(
            self.customer_id, "", "fake-token-id")])
        self.assertListEqual(cmock.call_args_list, [])

        # check that the subscription object was not created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(
                member=Alumni.objects.first())

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(None, Exception('Debug Error')))
    def test_signup_card_error_create_subscription(self, cmock, umock):
        # fill out and submit card details
        self.sget('setup_subscription', '#id_payment_type')
        self.submit_card_details()

        # check that things are as expected
        self.assertEqual(self.current_url, reverse('setup_subscription'),
                         'Check that the user stays on the subscribe page')

        # check that only the first mock was called
        self.assertListEqual(umock.call_args_list, [mock.call(
            self.customer_id, "", "fake-token-id")])
        self.assertListEqual(cmock.call_args_list, [mock.call(
            self.customer_id, self.subscribe_field_value)])

        # check that the subscription object was not created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(
                member=Alumni.objects.first())

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(MOCKED_SUBSCRIPTION, None))
    def test_signup_sepa(self, cmock, umock):
        self.sget('setup_subscription', '#id_payment_type')
        self.submit_sepa_details()

        # check that things are as expected
        self.assertEqual(self.current_url, reverse('setup_setup'),
                         'Check that the user gets redirected to the completed page')

        # check that the mocks were called
        self.assertListEqual(umock.call_args_list, [mock.call(
            self.customer_id, "fake-source-id", "")])
        self.assertListEqual(cmock.call_args_list, [mock.call(
            self.customer_id, self.subscribe_field_value)])

        # check that the subscription object was created
        obj = SubscriptionInformation.objects.get(
            member=Alumni.objects.first())
        self.assertEqual(obj.start, MOCKED_TIME)
        self.assertEqual(obj.end, None)
        self.assertEqual(obj.subscription, 'sub_fake')
        self.assertEqual(obj.external, False)
        self.assertEqual(obj.tier, self.tier_field_value)

    @mock.patch('django.utils.timezone.now',
                mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure')))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(MOCKED_SUBSCRIPTION, None))
    def test_signup_sepa_error_update_method(self, cmock, umock):
        # fill out and submit sepa details
        self.sget('setup_subscription', '#id_payment_type')
        self.submit_sepa_details()

        # check that things are as expected
        self.assertEqual(self.current_url, reverse('setup_subscription'),
                         'Check that the user stays on the first page')

        # check that only the first mock was called
        self.assertListEqual(umock.call_args_list, [mock.call(
            self.customer_id, "fake-source-id", "")])
        self.assertListEqual(cmock.call_args_list, [])

        # check that the subscription object was not created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(
                member=Alumni.objects.first())

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(None, Exception('Debug Error')))
    def test_signup_sepa_error_create_subscription(self, cmock, umock):
        # fill out and submit card details
        self.sget('setup_subscription', '#id_payment_type')
        self.submit_sepa_details()

        # check that things are as expected
        self.assertEqual(self.current_url, reverse('setup_subscription'),
                         'Check that the user stays on the subscribe page')

        # check that only the first mock was called
        self.assertListEqual(umock.call_args_list, [mock.call(
            self.customer_id, "fake-source-id", "")])
        self.assertListEqual(cmock.call_args_list, [mock.call(
            self.customer_id, self.subscribe_field_value)])

        # check that the subscription object was not created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(
                member=Alumni.objects.first())


class ContributorSubscribeTest(SignupPaymentsTestMixin, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_07b_contributor.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')
        self.tier_field_value = TierField.CONTRIBUTOR
        self.subscribe_field_value = 'contributor-membership'
        self.customer_id = 'cus_Fq8yG7rLrc6sKZ'


class PatronSubscribeTest(SignupPaymentsTestMixin, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_07c_patron.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')
        self.tier_field_value = TierField.PATRON
        self.subscribe_field_value = 'patron-membership'
        self.customer_id = 'cus_Fq8yG7rLrc6sKZ'
