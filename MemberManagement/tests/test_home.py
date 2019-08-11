from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from .selenium import SeleniumTest


class MySeleniumTests(SeleniumTest, StaticLiveServerTestCase):

    def test_plain_homepage(self):
        """ Checks that the plain home page works as intended """

        # Check that the plain http response is code 200
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # check that the returned html is actually the homepage
        # by comparing the title
        page = self.sget("/", "body")
        self.assertEqual(
            self.selenium.title, "Home - Membership Portal - Jacobs University Bremen Alumni")
