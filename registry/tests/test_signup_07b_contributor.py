from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest

from unittest import mock

from alumni.models import Alumni
from alumni.fields.tier import TierField

from payments.models import SubscriptionInformation, MembershipInformation

MOCKED_CUSTOMER = mock.MagicMock(id='cus_Fq8yG7rLrc6sKZ')


class ContributorTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_06_atlas.json']
    user = 'Mounfem'

    def test_setup_contributor_elements(self):
        # fill out the form and select the contributor tier
        self.fill_out_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": 'Contributor – Standard membership for 39€ p.a.'
        })

        self.assert_element_not_displayed('#description-st')
        self.assert_element_displayed('#description-co')
        self.assert_element_not_displayed('#description-pa')

    @mock.patch('payments.stripewrapper.create_customer', return_value=(MOCKED_CUSTOMER, None))
    def test_setup_contributor(self, mocked):
        # fill out the form an select the contributor tier
        self.submit_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": 'Contributor – Standard membership for 39€ p.a.'
        })

        self.assert_url_equal('setup_subscription',
                                'Check that the user gets redirected to the subscription page')

        # check that the stripe api was called with the object as a parameter
        alumni = self.user.alumni
        mocked.assert_has_calls([mock.call(alumni)])

        # check that the membership object was created
        membership = alumni.membership
        self.assertEqual(membership.tier, TierField.CONTRIBUTOR)
        self.assertEqual(membership.customer, 'cus_Fq8yG7rLrc6sKZ')

        # Check that the subscription object was *not* created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(member=alumni)

    @mock.patch('payments.stripewrapper.create_customer', return_value=(None, "debug"))
    def test_setup_contributor_fail(self, mocked):
        # fill out the form an select the payments tier
        self.submit_form('setup_membership', 'input_id_submit', select_dropdowns={
            "id_tier": 'Contributor – Standard membership for 39€ p.a.'
        })

        # we stay on the same page
        self.assert_url_equal('setup_membership',
                                'Check that the user does not get redirected to the final page')

        # check that the stripe api was called with the object as a parameter
        alumni = self.user.alumni
        mocked.assert_has_calls([mock.call(alumni)])

        # Check that the membership object was *not* created
        with self.assertRaises(MembershipInformation.DoesNotExist):
            alumni.membership

        # Check that the subscription object was *not* created
        with self.assertRaises(SubscriptionInformation.DoesNotExist):
            SubscriptionInformation.objects.get(member=alumni)
