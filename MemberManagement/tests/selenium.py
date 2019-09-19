import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions


class SeleniumTest(object):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('PYTEST_FIREFOX_VISIBLE', None) != '1':
            options.add_argument('-headless')
        cls.selenium = Firefox(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # setup selenium cookies on first call
        self.selenium.delete_all_cookies()

    @property
    def current_url(self):
        """ The current url of the web browser, without the live server url """
        url = str(self.selenium.current_url)
        if url.startswith(self.live_server_url):
            return url[len(self.live_server_url):]
        return url

    def wait_for_element(self, selector, timeout=10):
        """ Waits for element to be visible and returns it """

        wait = WebDriverWait(self.selenium, timeout)
        element = wait.until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, selector)))
        return element

    def sget(self, url, selector=None, timeout=10):
        """
            Loads a URL using selenium from the live server and waits for the CSS selector (if any) to be available
            Returns the element selected, None if none is selected, or raises TimeoutException if a timeout occurs.
        """
        self.selenium.get(self.live_server_url + url)
        if selector is None:
            return None

        return self.wait_for_element(selector, timeout=timeout)

    def fill_out_form(self, url, submit_button=None, send_form_keys=None, select_dropdowns=None, select_checkboxes=None, script_value=None, timeout=10):
        """
            Loads a URL using selenium from the live server and waits for the element with the submit_button id to be
            available.
            Once available, uses send_keys to send strings to elements with ids as specificed by send_form_keys dict.
            Next, selects either one item by visible text, or muliple items by value, in dropdowns specified by the
            select_dropdowns element.
            Next, sets the selection state of checkboxes of elements with ids as specified by the select_checkboxes
            dict.
            Next, directly set the value attribute of elements refered to by the script_value dict.
            Finally returns the button element.
        """
        if submit_button is None:
            selector = None
        else:
            selector = '#{}'.format(submit_button)

        # get the element on the page
        button = self.sget(url, selector=selector, timeout=timeout)

        # send_keys to the specified form elements
        if send_form_keys is not None:
            for id_, value in send_form_keys.items():
                element = self.selenium.find_element_by_id(id_)
                element.clear()
                element.send_keys(value)

        # select inside the specified dropdowns
        if select_dropdowns is not None:
            for id_, value in select_dropdowns.items():
                select = Select(self.selenium.find_element_by_id(id_))

                # if we are a multiple select, deselect all of them
                if select.is_multiple:
                    select.deselect_all()

                if isinstance(value, str):
                    select.select_by_visible_text(value)
                else:
                    for v in value:
                        select.select_by_value(v)

        # select the checkboxes
        if select_checkboxes is not None:
            for id_, value in select_checkboxes.items():
                checkbox = self.selenium.find_element_by_id(id_)
                if checkbox.is_selected() != value:
                    checkbox.click()

        # set the scripted values
        if script_value is not None:
            for id_, value in script_value.items():
                element = self.selenium.find_element_by_id(id_)
                self.selenium.execute_script(
                    'arguments[0].value = arguments[1];', element, value)

        # return the button
        return button

    def submit_form(self, *args, timeout=10, **kwargs):
        """ Fills out and submit a form, then returns the body element of the submitted page """

        # fill out the form and click the submit button
        button = self.fill_out_form(*args, timeout=timeout, **kwargs)
        button.click()

        # wait for body to be visible
        return self.wait_for_element('body', timeout=timeout)
