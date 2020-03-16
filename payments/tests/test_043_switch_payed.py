from __future__ import annotations

from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone

from alumni.fields.tier import TierField
from MemberManagement.tests.integration import (IntegrationTest,
                                                IntegrationTestBase)

MOCKED_TIME = timezone.datetime(
    2020, 2, 4, 15, 52, 27, 62000, tzinfo=timezone.utc)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional
    from datetime import datetime


class SwitchTestBase(IntegrationTestBase):
    def setUp(self):
        super().setUp()

        self.start_subscription = self.user.alumni.subscription.subscription
        self.subscribe_field_value = TierField.get_stripe_id(
            self.__class__.target_tier)
        self.start_tier = self.user.alumni.membership.tier
        self.start_time = self.user.alumni.subscription.start
        self.end_time = self.user.alumni.subscription.end

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
            subscription, subscription=self.start_subscription, tier=self.start_tier, start=self.start_time, end=self.end_time)
        self.assertEqual(self.user.alumni.membership.tier, self.start_tier)

    def _assert_tier_changed(self) -> None:
        # check that the new subscription was created
        subscription = self.user.alumni.subscription
        self.assertEqual(self.user.alumni.membership.tier,
                         self.__class__.target_tier)
        self._assert_subscription_equal(
            subscription, tier=self.__class__.target_tier, subscription=self.start_subscription, start=MOCKED_TIME)

        # check that the old subscription was closed
        subscription = self.user.alumni.subscriptioninformation_set.exclude(
            pk=subscription.pk).get()
        self._assert_subscription_equal(
            subscription, subscription=self.start_subscription, tier=self.start_tier, start=self.start_time, end=MOCKED_TIME)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_subscription', return_value=(True, None))
    def test_switch_ok(self, umock: mock.Mock) -> None:
        # select to upgrade the membership
        self.submit_form('update_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(self.__class__.target_tier)
        })

        # check that the methods to downgrade were called
        umock.assert_has_calls(
            [mock.call(self.start_subscription, self.subscribe_field_value)])

        self.user.alumni.refresh_from_db()

        # check that we were redirected to the update_membership page
        self.assert_url_equal('update_membership')
        self.assert_element_exists('div.message.uk-alert-success')

        # check that the new subscription was created
        self._assert_tier_changed()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.update_subscription', return_value=(None, "Debug Test"))
    def test_switch_fail(self, umock: mock.Mock) -> None:
        # select to upgrade the membership
        self.submit_form('update_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(self.__class__.target_tier)
        })

        # check that the methods to downgrade were called
        umock.assert_has_calls(
            [mock.call(self.start_subscription, self.subscribe_field_value)])

        self.user.alumni.refresh_from_db()

        # check that we were redirected to the update_membership page
        self.assert_url_equal('update_membership')
        self.assert_element_exists('div.message.uk-alert-danger')

        # check that the new subscription was created
        self._assert_tier_unchanged()


class ContributorSwitchTest(SwitchTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'eilie'
    target_tier = TierField.PATRON


class PatronSwitchTest(SwitchTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Douner'
    target_tier = TierField.CONTRIBUTOR
