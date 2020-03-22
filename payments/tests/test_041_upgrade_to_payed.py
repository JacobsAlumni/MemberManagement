from __future__ import annotations
from typing import TYPE_CHECKING

from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone

from alumni.fields.tier import TierField
from MemberManagement.tests.integration import IntegrationTest

from .stripefrontend import StripeFrontendTestMixin

MOCKED_TIME = timezone.datetime(
    2020, 2, 4, 15, 52, 27, 62000, tzinfo=timezone.utc)

if TYPE_CHECKING:
    from typing import Optional
    from datetime import datetime


class UpgradeTestBase(StripeFrontendTestMixin):
    def setUp(self) -> None:
        super().setUp()

        self.start_tier: str = self.user.alumni.membership.tier
        self.subscribe_field_value: str = TierField.get_stripe_id(
            self.__class__.target_tier)

        self.start_time: datetime = self.user.alumni.subscription.start
        self.end_time: Optional[datetime] = self.user.alumni.subscription.end

    def _assert_subscription_equal(self, instance: SubscriptionInformation, tier: Optional[str] = None, subscription: Optional[str] = None, external: bool = False, start: Optional[datetime] = None, end: Optional[datetime] = None) -> None:
        """ Asserts that a subscription instance is equal"""

        self.assertEqual(instance.start, start)
        self.assertEqual(instance.end, end)
        self.assertEqual(instance.subscription, subscription)
        self.assertEqual(instance.external, external)
        self.assertEqual(instance.tier, tier)

    def _assert_tier_unchanged(self) -> None:
        """ Asserts that the tier is still the original tier and has not changed """

        subscription = self.user.alumni.subscription
        self._assert_subscription_equal(
            subscription, tier=self.start_tier, start=self.start_time, end=self.end_time)
        self.assertEqual(self.user.alumni.membership.tier, self.start_tier)

    def _assert_select_redirect_payment(self) -> None:
        """ Asserts that selecting an update redirects to the payment method """

        # select to upgrade the membership
        self.submit_form('update_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(self.__class__.target_tier)
        })

        # and check that we are on the right url
        self.assert_url_equal(
            'setup_subscription', 'Check that the user is directed to enter payment details')
        self.assert_element_exists('div.message.uk-alert-primary')

        # we are still on the original tier
        self._assert_tier_unchanged()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=('sub_fake', None))
    def test_upgrade_card_ok(self, cmock: mock.Mock, umock: mock.Mock) -> None:

        # start the upgrade process and submit card details
        self._assert_select_redirect_payment()
        self.submit_card_details()
        self.user.alumni.refresh_from_db()

        # check that the mocks were called
        umock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, "", "fake-token-id")])
        cmock.assert_has_calls([mock.call(
            self.user.alumni.membership.customer, self.subscribe_field_value)])

        # check that the user is on the right page
        self.assert_url_equal('update_membership',
                              'Check that the user was redirected to the update membership page')
        self.assert_element_exists('div.message.uk-alert-success')

        # check that the new subscription was created
        subscription = self.user.alumni.subscription
        self.assertEqual(self.user.alumni.membership.tier,
                         self.__class__.target_tier)
        self._assert_subscription_equal(
            subscription, tier=self.__class__.target_tier, subscription='sub_fake', start=MOCKED_TIME)

        # check that the old subscription was closed
        subscription = self.user.alumni.subscriptioninformation_set.exclude(
            pk=subscription.pk).get()
        self._assert_subscription_equal(
            subscription, tier=self.start_tier, start=self.start_time, end=MOCKED_TIME)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure')))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=('sub_fake', None))
    def test_upgrade_card_error_update_method(self, cmock: mock.Mock, umock: mock.Mock) -> None:
        # start the upgrade process and submit card details
        self._assert_select_redirect_payment()
        self.submit_card_details()
        self.user.alumni.refresh_from_db()

        # check that only the first mock was called
        umock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, "", "fake-token-id")])
        cmock.assert_not_called()

        # check that things are as expected
        self.assert_url_equal('setup_subscription',
                              'Check that the user stays on the subscribe page')

        # we are still on the original tier
        self._assert_tier_unchanged()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(None, Exception('Debug Error')))
    def test_upgrade_card_error_create_subscription(self, cmock: mock.Mock, umock: mock.Mock) -> None:
        # start the upgrade process and submit card details
        self._assert_select_redirect_payment()
        self.submit_card_details()
        self.user.alumni.refresh_from_db()

        # check that only the first mock was called
        umock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, "", "fake-token-id")])
        cmock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, self.subscribe_field_value)])

        # check that things are as expected
        self.assert_url_equal('setup_subscription',
                              'Check that the user stays on the subscribe page')

        # we are still on the original tier
        self._assert_tier_unchanged()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=('sub_fake', None))
    def test_upgrade_sepa(self, cmock: mock.Mock, umock: mock.Mock) -> None:
        # start the upgrade process and submit card details
        self._assert_select_redirect_payment()
        self.submit_sepa_details()
        self.user.alumni.refresh_from_db()

        # check that the mocks were called
        umock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, "fake-source-id", "")])
        cmock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, self.subscribe_field_value)])

        # check that the user is on the right page
        self.assert_url_equal('update_membership',
                              'Check that the user was redirected to the update membership page')
        self.assert_element_exists('div.message.uk-alert-success')

        # check that the new subscription was created
        subscription = self.user.alumni.subscription
        self.assertEqual(self.user.alumni.membership.tier,
                         self.__class__.target_tier)
        self._assert_subscription_equal(
            subscription, tier=self.__class__.target_tier, subscription='sub_fake', start=MOCKED_TIME)

        # check that the old subscription was closed
        subscription = self.user.alumni.subscriptioninformation_set.exclude(
            pk=subscription.pk).get()
        self._assert_subscription_equal(
            subscription, tier=self.start_tier, start=self.start_time, end=MOCKED_TIME)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure')))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=('sub_fake', None))
    def test_upgrade_sepa_error_update_method(self, cmock: mock.Mock, umock: mock.Mock) -> None:
        # start the upgrade process and submit card details
        self._assert_select_redirect_payment()
        self.submit_sepa_details()
        self.user.alumni.refresh_from_db()

        # check that only the first mock was called
        umock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, "fake-source-id", "")])
        cmock.assert_not_called()

        # check that things are as expected
        self.assert_url_equal('setup_subscription',
                              'Check that the user stays on the first page')

        # nothing has changed
        self._assert_tier_unchanged()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(None, Exception('Debug Error')))
    def test_upgrade_sepa_error_create_subscription(self, cmock: mock.Mock, umock: mock.Mock) -> None:
        # start the upgrade process and submit card details
        self._assert_select_redirect_payment()
        self.submit_sepa_details()
        self.user.alumni.refresh_from_db()

        # check that only the first mock was called
        umock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, "fake-source-id", "")])
        cmock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer, self.subscribe_field_value)])

        # check that things are as expected
        self.assert_url_equal('setup_subscription',
                              'Check that the user stays on the subscribe page')

        # nothing has changed
        self._assert_tier_unchanged()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None))
    @mock.patch('payments.stripewrapper.create_subscription', return_value=(None, None))
    def test_cancel(self, cmock: mock.Mock, umock: mock.Mock) -> None:
        self._assert_select_redirect_payment()
        self.submit_cancel()

        # check that we get back to the subscription
        self.assert_url_equal('update_membership',
                              'Check that the user is sent back on the update membership page')
        self.assert_element_exists('div.message.uk-alert-success')

        # check that the mocks were called
        umock.assert_not_called()
        cmock.assert_not_called()

        # check that we are on the right tier
        self._assert_tier_unchanged()


class ContributorUpgradeTest(UpgradeTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Irew1996'
    target_tier = TierField.CONTRIBUTOR


class PatronUpgradeTest(UpgradeTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Irew1996'
    target_tier = TierField.PATRON
