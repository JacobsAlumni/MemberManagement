from __future__ import annotations

import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from MemberManagement.tests.integration import IntegrationTest


class CookieTest(IntegrationTest, StaticLiveServerTestCase):
    def test_cookiebanner_works(self) -> None:

        # check that loading the page for the first time shows the banner
        self.load_live_url("root")
        self.assert_element_displayed("#CookielawBanner")

        # reload the page, it should still be there
        self.load_live_url("root")
        self.assert_element_displayed("#CookielawBanner")

        # click the button, it should be hidden
        self.find_element("#CookielawBanner > p > button").click()
        time.sleep(1.0)  # wait for the element to disappear
        self.assert_element_not_displayed("#CookielawBanner")

        # reload the page, it should no longer be there
        self.load_live_url("root")
        self.assert_element_not_exists("#CookielawBanner")
