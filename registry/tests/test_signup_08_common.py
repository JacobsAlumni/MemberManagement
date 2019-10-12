from selenium.webdriver.support.ui import Select

class CommonSignupTest:
    def test_select_card(self):
        element = self.sget('/payments/subscribe/', '#id_payment_type')
        submit = self.wait_for_element('#button_id_presubmit', clickable=True)

        # select debit card payment method
        Select(element).select_by_visible_text('Credit or Debit Card')

        self.assertTrue(self.selenium.find_element_by_id(
            'stripe-card-elements').is_displayed())
        self.assertFalse(self.selenium.find_element_by_id(
            'stripe-iban-elements').is_displayed())

    def test_select_iban(self):
        element = self.sget('/payments/subscribe/', '#id_payment_type')
        submit = self.wait_for_element('#button_id_presubmit', clickable=True)

        # select debit card payment method
        Select(element).select_by_visible_text('Automatic Bank Transfer (SEPA)')

        self.assertFalse(self.selenium.find_element_by_id(
            'stripe-card-elements').is_displayed())
        self.assertTrue(self.selenium.find_element_by_id(
            'stripe-iban-elements').is_displayed())

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
        self.selenium.find_element_by_name(
            'cardnumber').send_keys('4242 4242 4242 4242')
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
        Select(element).select_by_visible_text(
            'Automatic Bank Transfer (SEPA)')

        # select the iban frame and fill out the fake data
        frame = self.wait_for_element('iframe[name=__privateStripeFrame6]')
        self.selenium.switch_to.frame(frame_reference=frame)
        self.selenium.find_element_by_name(
            'iban').send_keys('DE89370400440532013000')
        self.selenium.switch_to.default_content()

        # fill out the name
        self.wait_for_element('#name').send_keys('Anna Freytag')

        # submit the form
        submit.click()
