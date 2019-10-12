from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone

from alumni.fields.tier import TierField
from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest
from payments.models import SubscriptionInformation

from .test_signup_08_common import CommonSignupTest

MOCKED_TIME = timezone.datetime(
    2019, 9, 19, 16, 41, 17, 40, tzinfo=timezone.utc)
MOCKED_SUBSCRIPTION = mock.MagicMock(id='sub_fake')


class PatronSubscribeTest(CommonSignupTest, IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_07c_patron.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_signup_card_ok(self):
        with mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None)) as umock:
            with mock.patch('payments.stripewrapper.create_subscription', return_value=(MOCKED_SUBSCRIPTION, None)) as cmock:
                # fill out and submit card details
                self.submit_card_details()

                # check that things are as expected
                self.assertEqual(self.current_url, '/portal/setup/completed/',
                                 'Check that the user gets redirected to the completed page')

                # check that the mocks were called
                self.assertListEqual(umock.call_args_list, [mock.call(
                    "cus_Fq8yG7rLrc6sKZ", "", "fake-token-id")])
                self.assertListEqual(cmock.call_args_list, [mock.call(
                    "cus_Fq8yG7rLrc6sKZ", "patron-membership")])

                # check that the subscription object was created
                obj = SubscriptionInformation.objects.get(
                    member=Alumni.objects.first())
                self.assertEqual(obj.start, MOCKED_TIME)
                self.assertEqual(obj.end, None)
                self.assertEqual(obj.subscription, 'sub_fake')
                self.assertEqual(obj.external, False)
                self.assertEqual(obj.tier, TierField.PATRON)

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_signup_card_error_update_method(self):
        with mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure'))) as umock:
            with mock.patch('payments.stripewrapper.create_subscription', return_value=(MOCKED_SUBSCRIPTION, None)) as cmock:
                # fill out and submit card details
                self.submit_card_details()

                # check that things are as expected
                self.assertEqual(self.current_url, '/payments/subscribe/',
                                 'Check that the user stays on the first page')

                # check that only the first mock was called
                self.assertListEqual(umock.call_args_list, [mock.call(
                    "cus_Fq8yG7rLrc6sKZ", "", "fake-token-id")])
                self.assertListEqual(cmock.call_args_list, [])

                # check that the subscription object was not created
                with self.assertRaises(SubscriptionInformation.DoesNotExist):
                    SubscriptionInformation.objects.get(
                        member=Alumni.objects.first())

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_signup_card_error_create_subscription(self):
        with mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None)) as umock:
            with mock.patch('payments.stripewrapper.create_subscription', return_value=(None, Exception('Debug Error'))) as cmock:
                # fill out and submit card details
                self.submit_card_details()

                # check that things are as expected
                self.assertEqual(self.current_url, '/payments/subscribe/',
                                 'Check that the user stays on the subscribe page')

                # check that only the first mock was called
                self.assertListEqual(umock.call_args_list, [mock.call(
                    "cus_Fq8yG7rLrc6sKZ", "", "fake-token-id")])
                self.assertListEqual(cmock.call_args_list, [mock.call(
                    "cus_Fq8yG7rLrc6sKZ", "patron-membership")])

                # check that the subscription object was not created
                with self.assertRaises(SubscriptionInformation.DoesNotExist):
                    SubscriptionInformation.objects.get(
                        member=Alumni.objects.first())

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_signup_sepa(self):
        with mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None)) as umock:
            with mock.patch('payments.stripewrapper.create_subscription', return_value=(MOCKED_SUBSCRIPTION, None)) as cmock:
                self.submit_sepa_details()

                # check that things are as expected
                self.assertEqual(self.current_url, '/portal/setup/completed/',
                                 'Check that the user gets redirected to the completed page')

                # check that the mocks were called
                self.assertListEqual(umock.call_args_list, [mock.call(
                    "cus_Fq8yG7rLrc6sKZ", "fake-source-id", "")])
                self.assertListEqual(cmock.call_args_list, [mock.call(
                    "cus_Fq8yG7rLrc6sKZ", "patron-membership")])

                # check that the subscription object was created
                obj = SubscriptionInformation.objects.get(
                    member=Alumni.objects.first())
                self.assertEqual(obj.start, MOCKED_TIME)
                self.assertEqual(obj.end, None)
                self.assertEqual(obj.subscription, 'sub_fake')
                self.assertEqual(obj.external, False)
                self.assertEqual(obj.tier, TierField.PATRON)

    mock.patch('django.utils.timezone.now',
               mock.Mock(return_value=MOCKED_TIME))

    def test_signup_sepa_error_update_method(self):
        with mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure'))) as umock:
            with mock.patch('payments.stripewrapper.create_subscription', return_value=(MOCKED_SUBSCRIPTION, None)) as cmock:
                # fill out and submit sepa details
                self.submit_sepa_details()

                # check that things are as expected
                self.assertEqual(self.current_url, '/payments/subscribe/',
                                 'Check that the user stays on the first page')

                # check that only the first mock was called
                self.assertListEqual(umock.call_args_list, [mock.call(
                    "cus_Fq8yG7rLrc6sKZ", "fake-source-id", "")])
                self.assertListEqual(cmock.call_args_list, [])

                # check that the subscription object was not created
                with self.assertRaises(SubscriptionInformation.DoesNotExist):
                    SubscriptionInformation.objects.get(
                        member=Alumni.objects.first())

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_signup_sepa_error_create_subscription(self):
        with mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None)) as umock:
            with mock.patch('payments.stripewrapper.create_subscription', return_value=(None, Exception('Debug Error'))) as cmock:
                # fill out and submit card details
                self.submit_sepa_details()

                # check that things are as expected
                self.assertEqual(self.current_url, '/payments/subscribe/',
                                 'Check that the user stays on the subscribe page')

                # check that only the first mock was called
                self.assertListEqual(umock.call_args_list, [mock.call(
                    "cus_Fq8yG7rLrc6sKZ", "fake-source-id", "")])
                self.assertListEqual(cmock.call_args_list, [mock.call(
                    "cus_Fq8yG7rLrc6sKZ", "patron-membership")])

                # check that the subscription object was not created
                with self.assertRaises(SubscriptionInformation.DoesNotExist):
                    SubscriptionInformation.objects.get(
                        member=Alumni.objects.first())
