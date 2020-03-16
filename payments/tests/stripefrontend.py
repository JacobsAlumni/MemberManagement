from __future__ import annotations

from selenium.webdriver.support.ui import Select
from MemberManagement.tests.integration import IntegrationTestBase

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional


class StripeFrontendTestMixin(IntegrationTestBase):
    _payment_type_element = '#id_payment_type'
    _submit_button_element = '#button_id_presubmit'

    def assert_card_selectable(self) -> None:
        element = self.find_element(self.__class__._payment_type_element)
        submit = self.find_element('#button_id_presubmit', clickable=True)

        # select debit card payment method
        Select(element).select_by_visible_text('Credit or Debit Card')

        self.assert_element_displayed('#stripe-card-elements')
        self.assert_element_not_displayed('#stripe-iban-elements')

    def assert_iban_selectable(self) -> None:
        element = self.find_element(self.__class__._payment_type_element)
        submit = self.find_element(
            self.__class__._submit_button_element, clickable=True)

        # select debit card payment method
        Select(element).select_by_visible_text(
            'Automatic Bank Transfer (SEPA)')

        self.assert_element_not_displayed('#stripe-card-elements')
        self.assert_element_displayed('#stripe-iban-elements')

    def submit_card_details(self, cardnumber: str = '4242 4242 4242 4242', exp_date: str = '12/50', cvc: str = '123', postal: str = '12345', next_selector: Optional[str] = None) -> None:
        """ Fills out and submits testing card details """

        # load the subscribe page and wait for the submit button to be clickable
        element = self.find_element(self.__class__._payment_type_element)
        submit = self.find_element(
            self.__class__._submit_button_element, clickable=True)

        # select debit card payment method
        Select(element).select_by_visible_text('Credit or Debit Card')

        # select the card frame and fill out the fake data
        frame = self.find_element('iframe[name=__privateStripeFrame5]')
        self.selenium.switch_to.frame(frame_reference=frame)
        self.find_element('*[name=cardnumber]').send_keys(cardnumber)
        self.find_element('*[name=exp-date]').send_keys(exp_date)
        self.find_element('*[name=cvc]').send_keys(cvc)
        self.find_element('*[name=postal]').send_keys(postal)
        self.selenium.switch_to.default_content()

        # submit the form and wait for the next page to load
        submit.click()
        self.find_element(
            next_selector or self.__class__._find_element_selector)

    def submit_sepa_details(self, iban: str = 'DE89370400440532013000', name: str = 'Anna Freytag', next_selector: Optional[str] = None) -> None:
        """ Fills out and submits testing SEPA details """

        # load the subscribe page and wait for the submit button to be clickable
        element = self.find_element(self.__class__._payment_type_element)
        submit = self.find_element(
            self.__class__._submit_button_element, clickable=True)

        # select sepa payment method
        Select(element).select_by_visible_text(
            'Automatic Bank Transfer (SEPA)')

        # select the iban frame and fill out the fake data
        frame = self.find_element('iframe[name=__privateStripeFrame6]')
        self.selenium.switch_to.frame(frame_reference=frame)
        self.find_element('*[name=iban]').send_keys(iban)
        self.selenium.switch_to.default_content()

        # fill out the name
        self.find_element('#name').send_keys(name)

        # submit the form
        submit.click()
        self.find_element(
            next_selector or self.__class__._find_element_selector)
