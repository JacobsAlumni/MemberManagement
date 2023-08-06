from __future__ import annotations

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from MemberManagement.tests.integration import IntegrationTest, IntegrationTestBase

from unittest import mock

from datetime import timezone, datetime

METHODS_TABLE = [
    {
        "kind": "card",
        "brand": "visa",
        "exp_month": 8,
        "exp_year": 2021,
        "last4": "4242",
    },
    {
        "kind": "sepa",
        "last4": "1234",
        "mandate_reference": "00000000000000000000000",
        "mandate_url": "https://example.com/mandate",
    },
]

PAYMENTS_TABLE = [
    {
        "lines": [
            mock.MagicMock(
                description="1 x Patron Membership (Dec. 3, 2018 - Dec. 3, 2019)"
            )
        ],
        "date": 543795200,
        "total": [3900, "eur"],
        "paid": True,
        "closed": True,
        "upcoming": False,
    }
]

MOCKED_TIME = datetime(2019, 9, 19, 16, 41, 17, 40, tzinfo=timezone.utc)


class ViewPaymentsTestBase(IntegrationTestBase):
    fixtures = ["registry/tests/fixtures/integration.json"]
    expect_update_enabled = None

    @mock.patch("django.utils.timezone.now", mock.Mock(return_value=MOCKED_TIME))
    @mock.patch(
        "payments.stripewrapper.get_methods_table", return_value=(METHODS_TABLE, None)
    )
    @mock.patch(
        "payments.stripewrapper.get_payment_table", return_value=(PAYMENTS_TABLE, None)
    )
    def test_both_ok(self, mmock: mock.Mock, pmock: mock.Mock) -> None:
        self.load_live_url("view_payments")

        # ensure that both payment methods are shown
        self.assert_element_exists("#id_payment_method_1")
        self.assert_element_exists("#id_payment_method_2")

        # check that the update payment button is shown
        if self.__class__.expect_updatepayment_enabled:
            self.assert_element_exists("#id_update_payment")
        else:
            self.assert_element_not_exists("#id_update_payment")

        # check that the update tier button is shown
        if self.__class__.expect_updatetier_enabled:
            self.assert_element_exists("#id_update_tier")
        else:
            self.assert_element_not_exists("#id_update_tier")

        # and the invoice is visible too
        self.assert_element_exists("#id_invoice_1")

    @mock.patch("django.utils.timezone.now", mock.Mock(return_value=MOCKED_TIME))
    @mock.patch(
        "payments.stripewrapper.get_methods_table", return_value=(None, "Debug")
    )
    @mock.patch(
        "payments.stripewrapper.get_payment_table", return_value=(PAYMENTS_TABLE, None)
    )
    def test_payment_ok(self, mmock: mock.Mock, pmock: mock.Mock) -> None:
        self.load_live_url("view_payments")

        # ensure that both payment methods are shown
        self.assert_element_not_exists("#id_payment_method_1")
        self.assert_element_not_exists("#id_payment_method_2")
        self.assert_element_not_exists("#id_update_payment")
        self.assert_element_not_exists("#id_invoice_1")

    @mock.patch("django.utils.timezone.now", mock.Mock(return_value=MOCKED_TIME))
    @mock.patch(
        "payments.stripewrapper.get_methods_table",
        return_value=(METHODS_TABLE, "Debug"),
    )
    @mock.patch(
        "payments.stripewrapper.get_payment_table", return_value=(None, "Debug")
    )
    def test_methods_ok(self, mmock: mock.Mock, pmock: mock.Mock) -> None:
        self.load_live_url("view_payments")

        # ensure that both payment methods are shown
        self.assert_element_not_exists("#id_payment_method_1")
        self.assert_element_not_exists("#id_payment_method_2")
        self.assert_element_not_exists("#id_update_payment")
        self.assert_element_not_exists("#id_invoice_1")


class ViewStarterPayments(
    ViewPaymentsTestBase, IntegrationTest, StaticLiveServerTestCase
):
    user = "Ramila"
    expect_updatepayment_enabled = False
    expect_updatetier_enabled = True


class ViewContributorPayments(
    ViewPaymentsTestBase, IntegrationTest, StaticLiveServerTestCase
):
    user = "eilie"
    expect_updatepayment_enabled = True
    expect_updatetier_enabled = True


class ViewPatronPayments(
    ViewPaymentsTestBase, IntegrationTest, StaticLiveServerTestCase
):
    user = "Douner"
    expect_updatepayment_enabled = True
    expect_updatetier_enabled = True
