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
    2020, 2, 4, 15, 52, 27, 62000, tzinfo=timezone.utc)


class SignupPaymentsTestMixin(PaymentMethodTest):
    def test_card_ok(self):
        self.sget('update_subscription', '#id_payment_type')
        self.assert_card_selectable()

    def test_iban_ok(self):
        self.sget('update_subscription', '#id_payment_type')
        self.assert_iban_selectable()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    def test_signup_card_ok(self, umock):
        # fill out and submit card details
        self.sget('update_subscription', '#id_payment_type')
        self.submit_card_details()

        # check that we stayed on the same page and a success message appeared
        self.assertEqual(self.current_url, reverse('update_subscription'),
                         'Check that the user gets redirected to the update payments page')
        self.assertTrue(self.element_exists('article > div.uk-alert-success'))

        # check that the mock was called
        self.assertListEqual(umock.call_args_list, [mock.call(
            self.customer_id, '', "fake-token-id")])

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure')))
    def test_signup_card_error_update_method(self, umock):
        # fill out and submit card details
        self.sget('update_subscription', '#id_payment_type')
        self.submit_card_details()

        # check that we stayed on the same page and a warning message appeared
        self.assertEqual(self.current_url, reverse('update_subscription'),
                         'Check that the user gets redirected to the update payments page')
        self.assertTrue(self.element_exists(
            'article > div > form > div.uk-alert-danger'))

        # check that only the mock was called
        self.assertListEqual(umock.call_args_list, [mock.call(
            self.customer_id, "", "fake-token-id")])

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    def test_signup_sepa_ok(self, umock):
        # fill out and submit card details
        self.sget('update_subscription', '#id_payment_type')
        self.submit_sepa_details()

        # check that we stayed on the same page and a success message appeared
        self.assertEqual(self.current_url, reverse('update_subscription'),
                         'Check that the user gets redirected to the update payments page')
        self.assertTrue(self.element_exists('article > div.uk-alert-success'))

        # check that the mock was called
        self.assertListEqual(umock.call_args_list, [mock.call(
            self.customer_id, "fake-source-id", '')])

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure')))
    def test_signup_sepa_error_update_method(self, umock):
        # fill out and submit card details
        self.sget('update_subscription', '#id_payment_type')
        self.submit_sepa_details()

        # check that we stayed on the same page and a warning message appeared
        self.assertEqual(self.current_url, reverse('update_subscription'),
                         'Check that the user gets redirected to the update payments page')
        self.assertTrue(self.element_exists(
            'article > div > form > div.uk-alert-danger'))

        # check that only the mock was called
        self.assertListEqual(umock.call_args_list, [mock.call(
            self.customer_id, "fake-source-id", '')])


class ContributorUpdateTest(SignupPaymentsTestMixin, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']

    def setUp(self):
        super().setUp()
        self.user = self.login('eilie')
        self.alumni = self.user.alumni
        self.customer_id = 'cus_GfpLiO9Z2SfL3P'


class PatronUpdateTest(SignupPaymentsTestMixin, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']

    def setUp(self):
        super().setUp()
        self.user = self.login('Douner')
        self.alumni = self.user.alumni
        self.customer_id = 'cus_GfpO5cARosOXVD'
