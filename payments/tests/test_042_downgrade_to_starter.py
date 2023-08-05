from __future__ import annotations

from datetime import timedelta
from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from datetime import timezone, datetime

from alumni.fields.tier import TierField
from MemberManagement.tests.integration import (IntegrationTest,
                                                IntegrationTestBase)

MOCKED_TIME = datetime(
    2020, 2, 4, 15, 52, 27, 62000, tzinfo=timezone.utc)
MOCKED_END = MOCKED_TIME + timedelta(days=2 * 365)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional
    from datetime import datetime

class DowngradeTestBase(IntegrationTestBase):
    def setUp(self) -> None:
        super().setUp()

        self.start_subscription: str = self.user.alumni.subscription.subscription
        self.start_tier: str = self.user.alumni.membership.tier
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
            subscription, subscription=self.start_subscription, tier=self.start_tier, start=self.start_time, end=self.end_time)
        self.assertEqual(self.user.alumni.membership.tier, self.start_tier)

    def _assert_tier_changed(self) -> None:
        # check that the new subscription was created
        subscription = self.user.alumni.subscription
        self.assertEqual(self.user.alumni.membership.tier, TierField.STARTER)
        self._assert_subscription_equal(
            subscription, tier=TierField.STARTER, subscription=None, start=MOCKED_TIME, end=MOCKED_END)

        # check that the old subscription was closed
        subscription = self.user.alumni.subscriptioninformation_set.exclude(
            pk=subscription.pk).get()
        self._assert_subscription_equal(
            subscription, subscription=self.start_subscription, tier=self.start_tier, start=self.start_time, end=MOCKED_TIME)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.cancel_subscription', return_value=(True, None))
    @mock.patch('payments.stripewrapper.clear_all_payment_sources', return_value=(True, None))
    def test_downgrade_ok(self, pmock: mock.Mock, smock: mock.Mock) -> None:
        # select to downgrade the membership
        self.submit_form('update_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(TierField.STARTER)
        })

        # check that the methods to downgrade were called
        smock.assert_has_calls([mock.call(self.start_subscription)])
        pmock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer)])

        self.user.alumni.refresh_from_db()

        # check that we were redirected to the update_membership page
        self.assert_url_equal('update_membership')
        self.assert_element_exists('div.message.uk-alert-success')

        # check that the new subscription was created
        self._assert_tier_changed()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.cancel_subscription', return_value=(None, "Testing Failure"))
    @mock.patch('payments.stripewrapper.clear_all_payment_sources', return_value=(True, None))
    def test_downgrade_fail_cancel(self, pmock: mock.Mock, smock: mock.Mock) -> None:
        # select to downgrade the membership
        self.submit_form('update_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(TierField.STARTER)
        })

        # check that the methods to downgrade were called
        smock.assert_has_calls([mock.call(self.start_subscription)])
        pmock.assert_not_called()

        self.user.alumni.refresh_from_db()

        # check that we were redirected to the update_membership page and shown an error
        self.assert_url_equal('update_membership')
        self.assert_element_exists('div .message.uk-alert-danger')

        # assert that the tier hasn't changed
        self._assert_tier_unchanged()

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    @mock.patch('payments.stripewrapper.cancel_subscription', return_value=(True, None))
    @mock.patch('payments.stripewrapper.clear_all_payment_sources', return_value=(None, "Debug Fail"))
    def test_downgrade_fail_clear(self, pmock: mock.Mock, smock: mock.Mock) -> None:
        # select to downgrade the membership
        self.submit_form('update_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(TierField.STARTER)
        })

        # check that the methods to downgrade were called
        smock.assert_has_calls([mock.call(self.start_subscription)])
        pmock.assert_has_calls(
            [mock.call(self.user.alumni.membership.customer)])

        self.user.alumni.refresh_from_db()

        # check that we were redirected to the update_membership page and shown an error
        self.assert_url_equal('update_membership')
        self.assert_element_exists('div.message.uk-alert-danger')

        # assert that the tier hasn't changed
        self._assert_tier_changed()


class ContributorDowngradeTest(DowngradeTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'eilie'


class PatronDowngradeTest(DowngradeTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Douner'
