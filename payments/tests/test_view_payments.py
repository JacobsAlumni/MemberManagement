from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest

from unittest import mock

from django.utils import timezone

METHODS_TABLE = [
    {
        'kind': 'card',
        'brand': 'visa',
        'exp_month': 8,
        'exp_year': 2021,
        'last4': '4242'
    },
    {
        'kind': 'sepa',
        'last4': '1234',
        'mandate_reference': '00000000000000000000000',
        'mandate_url': 'https://example.com/mandate',
    }
]

PAYMENTS_TABLE = [
    {
        'lines': [mock.MagicMock(description='1 x Patron Membership (Dec. 3, 2018 - Dec. 3, 2019)')],
        'date': 543795200,
        'total': [3900, 'eur'],
        'paid': True,
        'closed': True
    }
]

MOCKED_TIME = timezone.datetime(
    2019, 9, 19, 16, 41, 17, 40, tzinfo=timezone.utc)


class ViewPaymentsTestMixin:
    fixtures = ['registry/tests/fixtures/integration.json']

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.get_methods_table', return_value=(METHODS_TABLE, None))
    @mock.patch('payments.stripewrapper.get_payment_table', return_value=(PAYMENTS_TABLE, None))
    def test_both_ok(self, mmock, pmock):
        self.sget(reverse('view_payments'))

        # ensure that both payment methods are shown
        self.assertTrue(self.element_exists('#id_payment_method_1'))
        self.assertTrue(self.element_exists('#id_payment_method_2'))
        self.assertEqual(self.element_exists(
            '#id_update_payment'), self.payment_update_enabled)
        self.assertTrue(self.element_exists('#id_invoice_1'))

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.get_methods_table', return_value=(None, 'Debug'))
    @mock.patch('payments.stripewrapper.get_payment_table', return_value=(PAYMENTS_TABLE, None))
    def test_payment_ok(self, mmock, pmock):
        self.sget(reverse('view_payments'))

        # ensure that both payment methods are shown
        self.assertFalse(self.element_exists('#id_payment_method_1'))
        self.assertFalse(self.element_exists('#id_payment_method_2'))
        self.assertFalse(self.element_exists('#id_update_payment'))
        self.assertFalse(self.element_exists('#id_invoice_1'))

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.get_methods_table', return_value=(METHODS_TABLE, 'Debug'))
    @mock.patch('payments.stripewrapper.get_payment_table', return_value=(None, 'Debug'))
    def test_methods_ok(self, mmock, pmock):
        self.sget(reverse('view_payments'))

        # ensure that both payment methods are shown
        self.assertFalse(self.element_exists('#id_payment_method_1'))
        self.assertFalse(self.element_exists('#id_payment_method_2'))
        self.assertFalse(self.element_exists('#id_update_payment'))
        self.assertFalse(self.element_exists('#id_invoice_1'))


class ViewStarterPayments(ViewPaymentsTestMixin, IntegrationTest, StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.login('Ramila')
        self.payment_update_enabled = False


class ViewContributorPayments(ViewPaymentsTestMixin, IntegrationTest, StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.login('eilie')
        self.payment_update_enabled = True


class ViewPatronPayments(ViewPaymentsTestMixin, IntegrationTest, StaticLiveServerTestCase):
    def setUp(self):
        super().setUp()
        self.login('Douner')
        self.payment_update_enabled = True
