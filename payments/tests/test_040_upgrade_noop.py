from __future__ import annotations

from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone

from alumni.fields.tier import TierField
from MemberManagement.tests.integration import IntegrationTest

from .stripefrontend import StripeFrontendTestMixin

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datetime import datetime
    from typing import Optional
    from ..models import SubscriptionInformation

MOCKED_TIME = timezone.datetime(
    2020, 2, 4, 15, 52, 27, 62000, tzinfo=timezone.utc)


class UpgradeNoopTestBase(StripeFrontendTestMixin):
    def setUp(self) -> None:
        super().setUp()

        self.start_tier: str = self.user.alumni.membership.tier
        self.start_subscription: Optional[str] = self.user.alumni.subscription.subscription
        self.start_time: datetime = self.user.alumni.subscription.start
        self.end_time: Optional[datetime] = self.user.alumni.subscription.end

    def _assert_subscription_equal(self, instance: SubscriptionInformation, tier: Optional[str]=None, subscription: Optional[str]=None, external: bool=False, start: Optional[datetime]=None, end: Optional[datetime]=None) -> None:
        """ Asserts that a subscription instance is equal"""

        self.assertEqual(instance.start, start)
        self.assertEqual(instance.end, end)
        self.assertEqual(instance.subscription, subscription)
        self.assertEqual(instance.external, external)
        self.assertEqual(instance.tier, tier)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_noop_ok(self) -> None:
        self.mark_skippable()

        self.submit_form('update_membership', 'input_id_submit', select_dropdowns={
            "id_tier": TierField.get_description(self.start_tier)
        })

        # refresh the alumni
        self.user.alumni.refresh_from_db()

        # check that we were redirected to the update_membership page
        self.assert_url_equal('update_membership')
        self.assert_element_exists('div.message.uk-alert-success')

        # check that the new subscription was as expected
        subscription = self.user.alumni.subscription
        self._assert_subscription_equal(
            subscription, subscription=self.start_subscription, tier=self.start_tier, start=self.start_time, end=self.end_time)
        self.assertEqual(self.user.alumni.membership.tier, self.start_tier)


class StarterNoopTest(UpgradeNoopTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Ramila'


class ContributorNoopTest(UpgradeNoopTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'eilie'


class PatronNoopTest(UpgradeNoopTestBase, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Douner'
