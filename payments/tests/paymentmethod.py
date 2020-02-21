from selenium.webdriver.support.ui import Select

class PaymentMethodTest:
    def assert_card_selectable(self):
        element = self.find_element('#id_payment_type')
        submit = self.find_element('#button_id_presubmit', clickable=True)

        # select debit card payment method
        Select(element).select_by_visible_text('Credit or Debit Card')

        self.assert_element_displayed('#stripe-card-elements')
        self.assert_element_not_displayed('#stripe-iban-elements')

    def assert_iban_selectable(self):
        element = self.find_element('#id_payment_type')
        submit = self.find_element('#button_id_presubmit', clickable=True)

        # select debit card payment method
        Select(element).select_by_visible_text('Automatic Bank Transfer (SEPA)')

        self.assert_element_not_displayed('#stripe-card-elements')
        self.assert_element_displayed('#stripe-iban-elements')

    def submit_card_details(self):
        """ Fills out and submits testing card details """

        # load the subscribe page and wait for the submit button to be clickable
        element = self.find_element('#id_payment_type')
        submit = self.find_element('#button_id_presubmit', clickable=True)

        # select debit card payment method
        Select(element).select_by_visible_text('Credit or Debit Card')

        # select the card frame and fill out the fake data
        frame = self.find_element('iframe[name=__privateStripeFrame5]')
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
        element = self.find_element('#id_payment_type')
        submit = self.find_element('#button_id_presubmit', clickable=True)

        # select sepa payment method
        Select(element).select_by_visible_text(
            'Automatic Bank Transfer (SEPA)')

        # select the iban frame and fill out the fake data
        frame = self.find_element('iframe[name=__privateStripeFrame6]')
        self.selenium.switch_to.frame(frame_reference=frame)
        self.selenium.find_element_by_name(
            'iban').send_keys('DE89370400440532013000')
        self.selenium.switch_to.default_content()

        # fill out the name
        self.find_element('#name').send_keys('Anna Freytag')

        # submit the form
        submit.click()
