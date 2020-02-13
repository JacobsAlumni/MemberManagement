import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from MemberManagement.tests.integration import IntegrationTest


class CookieTest(IntegrationTest, StaticLiveServerTestCase):
    def test_cookiebanner_works(self):

        # check that loading the page for the first time shows the banner
        self.sget('root')
        self.assertTrue(self.selenium.find_element_by_id(
            'CookielawBanner').is_displayed())

        # reload the page, it should still be there
        self.sget('root')
        self.assertTrue(self.selenium.find_element_by_id(
            'CookielawBanner').is_displayed())

        # click the button, it should be hidden
        self.wait_for_element('#CookielawBanner > p > button').click()
        time.sleep(1.0)  # wait for the element to disappear
        self.assertFalse(self.selenium.find_element_by_id(
            'CookielawBanner').is_displayed())

        # reload the page, it should no longer be there
        self.sget('root')
        self.assertFalse(self.element_exists('#CookielawBanner'))
