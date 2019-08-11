from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class SeleniumTest(object):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('-headless')
        cls.selenium = Firefox(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def sget(self, url, selector=None, timeout=10):
        """
            Loads a URL using selenium from the live server and waits for the CSS selector (if any) to be available
            Returns the element selected, None if none is selected, or raises TimeoutException if a timeout occurs.
        """
        self.selenium.get(self.live_server_url + url)
        if selector is None:
            return None

        wait = WebDriverWait(self.selenium, timeout)
        element = wait.until(expected_conditions.visibility_of_element_located(
            (By.CSS_SELECTOR, selector)))
        return element
