from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone

from MemberManagement.tests.integration import IntegrationTest

from .stripefrontend import StripeFrontendTestMixin

MOCKED_TIME = timezone.datetime(
    2020, 2, 4, 15, 52, 27, 62000, tzinfo=timezone.utc)


class SignupPaymentsTestBase(StripeFrontendTestMixin):
    def test_card_ok(self):
        self.load_live_url('update_subscription', '#id_payment_type')
        self.assert_card_selectable()

    def test_iban_ok(self):
        self.load_live_url('update_subscription', '#id_payment_type')
        self.assert_iban_selectable()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    def test_signup_card_ok(self, umock):
        # fill out and submit card details
        self.load_live_url('update_subscription', '#id_payment_type')
        self.submit_card_details()

        # check that we stayed on the same page and a success message appeared
        self.assert_url_equal('update_subscription',
                              'Check that the user gets redirected to the update payments page')
        self.assert_element_exists('div.message.uk-alert-success')

        # check that the mock was called
        umock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, '', "fake-token-id")])

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure')))
    def test_signup_card_error_update_method(self, umock):
        # fill out and submit card details
        self.load_live_url('update_subscription', '#id_payment_type')
        self.submit_card_details()

        # check that we stayed on the same page and a warning message appeared
        self.assert_url_equal('update_subscription',
                              'Check that the user gets redirected to the update payments page')
        self.assert_element_exists(
            'article > div > form > div.uk-alert-danger')

        # check that only the mock was called
        umock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, "", "fake-token-id")])

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    def test_signup_sepa_ok(self, umock):
        # fill out and submit card details
        self.load_live_url('update_subscription', '#id_payment_type')
        self.submit_sepa_details()

        # check that we stayed on the same page and a success message appeared
        self.assert_url_equal('update_subscription',
                              'Check that the user gets redirected to the update payments page')
        self.assert_element_exists('div.message.uk-alert-success')

        # check that the mock was called
        umock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, "fake-source-id", '')])

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure')))
    def test_signup_sepa_error_update_method(self, umock):
        # fill out and submit card details
        self.load_live_url('update_subscription', '#id_payment_type')
        self.submit_sepa_details()

        # check that we stayed on the same page and a warning message appeared
        self.assert_url_equal('update_subscription',
                              'Check that the user gets redirected to the update payments page')
        self.assert_element_exists(
            'article > div > form > div.uk-alert-danger')

        # check that only the mock was called
        umock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, "fake-source-id", '')])


class ContributorUpdateTest(SignupPaymentsTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'eilie'


class PatronUpdateTest(SignupPaymentsTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Douner'
