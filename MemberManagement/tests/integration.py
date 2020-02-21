from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse
from django_selenium_clean import SeleniumTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait
from seleniumlogin import force_login


class IntegrationTest(SeleniumTestCase):
    """ An integration test base class using Selenium """

    user = None

    def setUp(self):
        # before each test case, we need to reset the cookies
        self.selenium.delete_all_cookies()

        user = self.__class__.user
        if user is not None:
            self.user = self.login(user)

    def load_fixture(self, path):
        """ Loads a fixture for use in unit tests """

        return call_command('loaddata', path)

    def login(self, username):
        """ Authenticates the user with the given username and returns the user object """

        # use the force_login method to enforce login
        user = get_user_model().objects.get(username=username)
        # TODO: Switch this to the appropriate django-selenium-clean method
        # once the PR gets merged
        force_login(user, self.selenium, self.live_server_url)

        return user

    @property
    def _current_url(self):
        """ The current url of the server relative to the root """
        url = str(self.selenium.current_url)
        if url.startswith(self.live_server_url):
            return url[len(self.live_server_url):]
        return url

    def assert_url_equal(self, url, *args, **kwargs):
        """ Asserts that the current url is equal to the (pontially resolvable) url """

        got = self._current_url
        expected = self._resolve_url(url, **kwargs)
        return self.assertEqual(got, expected, *args)

    def _element_exists(self, selector):
        """ Checks if an element with the given selector exists on the page """

        return len(self.selenium.find_elements(By.CSS_SELECTOR, selector)) > 0

    def _element_displayed(self, selector):
        """ Checks if an element with a given selector exists and is displayed """
        for element in self.selenium.find_elements(By.CSS_SELECTOR, selector):
            return element.is_displayed()
        return False

    def assert_element_exists(self, selector, *args):
        """ Asserts that an element exists on the current page """

        return self.assertTrue(self._element_exists(selector), *args)

    def assert_element_not_exists(self, selector, *args):
        """ Asserts that an element does not exist on the current page """

        return self.assertFalse(self._element_exists(selector), *args)

    def assert_element_displayed(self, selector, *args):
        """ Asserts that an element with the given selector is displayed """

        return self.assertTrue(self._element_displayed(selector), *args)

    def assert_element_not_displayed(self, selector, *args):
        """ Asserts that an element with the given selector is not displayed """

        return self.assertFalse(self._element_displayed(selector), *args)

    _find_element_timeout = 10
    _find_element_selector = '.main-container'

    def find_element(self, selector, timeout=None, clickable=False):
        """ Finds an element by a selector and waits for it to become available """
        if timeout is None:
            timeout = self.__class__._find_element_timeout
        if selector is None:
            selector = self.__class__._find_element_selector

        wait = WebDriverWait(self.selenium, timeout)

        if clickable:
            condition = expected_conditions.element_to_be_clickable
        else:
            condition = expected_conditions.visibility_of_element_located

        return wait.until(condition((By.CSS_SELECTOR, selector)))

    def _resolve_url(self, url, args=None, kwargs=None, reverse_get_params=None):
        """ Resolves a url pattern into a url """

        # If it's an absolute url, the test case is wrong
        if url.startswith('/'):
            raise AssertionError(
                '_resolve_url() does not accept absolute urls, got: {}'.format(url))

        # the url itself is resolved using 'reverse'
        resolved = reverse(url, args=args, kwargs=kwargs)

        # if we have 'reverse_get_params', reverse all of them
        if reverse_get_params is not None:
            resolved = resolved + '?' + '&'.join(['{}={}'.format(k, reverse(v)) for (k, v) in reverse_get_params.items()])

        # and return the resolved url
        return resolved

    def load_live_url(self, url_pattern, selector=None, url_args=None, url_kwargs=None, url_reverse_get_params=None, selector_timeout=None):
        """
            Loads an url from the selenium from the live server and waits for the CSS selector (if any) to be available
            Returns the element selected, None if none is selected, or raises TimeoutException if a timeout occurs.
        """

        # resolve the url and load it
        url = self._resolve_url(
            url_pattern, args=url_args, kwargs=url_kwargs, reverse_get_params=url_reverse_get_params)
        self.selenium.get(self.live_server_url + url)

        # wait for the element
        return self.find_element(selector, timeout=selector_timeout)

    def assert_url_follow(self, url, new_url, url_args=None, url_kwargs=None, url_reverse_get_params=None, new_url_args=None, new_url_kwargs=None, new_url_reverse_get_params=None, *args, url_selector=None, url_selector_timeout=None):
        """ Asserts that loading url (with selector selector) in the browser redirects to new_url
        """

        # load the url
        self.load_live_url(url, url_args=url_args, url_kwargs=url_kwargs, url_reverse_get_params=url_reverse_get_params,
                           selector=url_selector, selector_timeout=url_selector_timeout)

        # and check that it's equal
        return self.assert_url_equal(new_url, args=new_url_args, kwargs=new_url_kwargs, reverse_get_params=new_url_reverse_get_params, *args)

    def fill_out_form(self, url_pattern, submit_button=None, send_form_keys=None, select_dropdowns=None, select_checkboxes=None, script_value=None, selector=None, url_args=None, url_kwargs=None, url_reverse_get_params=None, selector_timeout=None):
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
        button = self.load_live_url(url_pattern, selector=selector, url_args=url_args, url_kwargs=url_kwargs,
                                    url_reverse_get_params=url_reverse_get_params, selector_timeout=selector_timeout)

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

                # if the value was set to none, do nothing
                if value is None:
                    continue

                # if we have a string, select by visible text
                if isinstance(value, str):
                    select.select_by_visible_text(value)

                # else select all the ones by the given value
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

    def submit_form(self, *args, next_selector=None, selector_timeout=None, **kwargs):
        """ Fills out and submit a form, then returns the body element of the submitted page """

        # fill out the form and click the submit button
        button = self.fill_out_form(*args, selector_timeout=selector_timeout, **kwargs)
        button.click()

        # wait for next element to be visible
        return self.find_element(next_selector, timeout=selector_timeout)

    def disable_form_requirements(self):
        self.selenium.execute_script("""
        var inputs = document.getElementsByTagName('input');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].removeAttribute('required');
        }
        var selects = document.getElementsByTagName('select');
        for (var i = 0; i < selects.length; i++) {
            selects[i].removeAttribute('required');
        }
        """)
