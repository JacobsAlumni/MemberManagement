from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest

from selenium.webdriver.support.ui import Select

from django.utils import timezone

from unittest import mock

from alumni.models import Alumni
from alumni.fields.tier import TierField

from payments.models import SubscriptionInformation

MOCKED_TIME = timezone.datetime(
    2019, 9, 19, 16, 41, 17, 40, tzinfo=timezone.utc)
MOCKED_SUBSCRIPTION = mock.MagicMock(id='sub_fake')


class ContributorSubscribeTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_07b_contributor.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')

    def submit_card_details(self):
        """ Fills out and submits testing card details """

        # load the subscribe page and wait for the submit button to be clickable
        element = self.sget('/payments/subscribe/', '#id_payment_type')
        submit = self.wait_for_element('#button_id_presubmit', clickable=True)

        # select debit card payment method
        Select(element).select_by_visible_text('Credit or Debit Card')

        # select the card frame and fill out the fake data
        frame = self.wait_for_element('iframe[name=__privateStripeFrame5]')
        self.selenium.switch_to.frame(frame_reference=frame)
        self.selenium.find_element_by_name('cardnumber').send_keys('4242 4242 4242 4242')
        self.selenium.find_element_by_name('exp-date').send_keys('12/50')
        self.selenium.find_element_by_name('cvc').send_keys('123')
        self.selenium.find_element_by_name('postal').send_keys('12345')
        self.selenium.switch_to.default_content()

        # submit the form
        submit.click()

    def submit_sepa_details(self):
        """ Fills out and submits testing SEPA details """

        # load the subscribe page and wait for the submit button to be clickable
        element = self.sget('/payments/subscribe/', '#id_payment_type')
        submit = self.wait_for_element('#button_id_presubmit', clickable=True)

        # select sepa payment method
        Select(element).select_by_visible_text('Automatic Bank Transfer (SEPA)')

        # select the iban frame and fill out the fake data
        frame = self.wait_for_element('iframe[name=__privateStripeFrame6]')
        self.selenium.switch_to.frame(frame_reference=frame)
        self.selenium.find_element_by_name('iban').send_keys('DE89370400440532013000')
        self.selenium.switch_to.default_content()

        # fill out the name
        self.wait_for_element('#name').send_keys('Anna Freytag')

        # submit the form
        submit.click()

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
                self.assertListEqual(umock.call_args_list, [mock.call("cus_Fq8yG7rLrc6sKZ", "", "fake-token-id")])
                self.assertListEqual(cmock.call_args_list, [mock.call("cus_Fq8yG7rLrc6sKZ", "contributor-membership")])

                # check that the subscription object was created
                obj = SubscriptionInformation.objects.get(member=Alumni.objects.first())
                self.assertEqual(obj.start, MOCKED_TIME)
                self.assertEqual(obj.end, None)
                self.assertEqual(obj.subscription, 'sub_fake')
                self.assertEqual(obj.external, False)
                self.assertEqual(obj.tier, TierField.CONTRIBUTOR)

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
                self.assertListEqual(umock.call_args_list, [mock.call("cus_Fq8yG7rLrc6sKZ", "", "fake-token-id")])
                self.assertListEqual(cmock.call_args_list, [])

                # check that the subscription object was not created
                with self.assertRaises(SubscriptionInformation.DoesNotExist):
                    SubscriptionInformation.objects.get(member=Alumni.objects.first())

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
                self.assertListEqual(umock.call_args_list, [mock.call("cus_Fq8yG7rLrc6sKZ", "", "fake-token-id")])
                self.assertListEqual(cmock.call_args_list, [mock.call("cus_Fq8yG7rLrc6sKZ", "contributor-membership")])

                # check that the subscription object was not created
                with self.assertRaises(SubscriptionInformation.DoesNotExist):
                    SubscriptionInformation.objects.get(member=Alumni.objects.first())

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_signup_sepa(self):
        with mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, None)) as umock:
            with mock.patch('payments.stripewrapper.create_subscription', return_value=(MOCKED_SUBSCRIPTION, None)) as cmock:
                self.submit_sepa_details()

                # check that things are as expected
                self.assertEqual(self.current_url, '/portal/setup/completed/',
                                'Check that the user gets redirected to the completed page')

                # check that the mocks were called
                self.assertListEqual(umock.call_args_list, [mock.call("cus_Fq8yG7rLrc6sKZ", "fake-source-id", "")])
                self.assertListEqual(cmock.call_args_list, [mock.call("cus_Fq8yG7rLrc6sKZ", "contributor-membership")])

                # check that the subscription object was created
                obj = SubscriptionInformation.objects.get(member=Alumni.objects.first())
                self.assertEqual(obj.start, MOCKED_TIME)
                self.assertEqual(obj.end, None)
                self.assertEqual(obj.subscription, 'sub_fake')
                self.assertEqual(obj.external, False)
                self.assertEqual(obj.tier, TierField.CONTRIBUTOR)

    mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_signup_sepa_error_update_method(self):
        with mock.patch('payments.stripewrapper.update_payment_method', return_value=(None, Exception('Debug failure'))) as umock:
            with mock.patch('payments.stripewrapper.create_subscription', return_value=(MOCKED_SUBSCRIPTION, None)) as cmock:
                # fill out and submit sepa details
                self.submit_sepa_details()

                # check that things are as expected
                self.assertEqual(self.current_url, '/payments/subscribe/',
                                'Check that the user stays on the first page')

                # check that only the first mock was called
                self.assertListEqual(umock.call_args_list, [mock.call("cus_Fq8yG7rLrc6sKZ", "fake-source-id", "")])
                self.assertListEqual(cmock.call_args_list, [])

                # check that the subscription object was not created
                with self.assertRaises(SubscriptionInformation.DoesNotExist):
                    SubscriptionInformation.objects.get(member=Alumni.objects.first())

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
                self.assertListEqual(umock.call_args_list, [mock.call("cus_Fq8yG7rLrc6sKZ", "fake-source-id", "")])
                self.assertListEqual(cmock.call_args_list, [mock.call("cus_Fq8yG7rLrc6sKZ", "contributor-membership")])

                # check that the subscription object was not created
                with self.assertRaises(SubscriptionInformation.DoesNotExist):
                    SubscriptionInformation.objects.get(member=Alumni.objects.first())
