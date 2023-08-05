from __future__ import annotations

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from MemberManagement.tests.integration import IntegrationTest

from alumni.models import Alumni
from selenium.webdriver.common.by import By

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List
    from django.db import models


class AdminTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Mounfem'

    def _assert_admin_results(self, model: str, objects: List[model.Model]) -> None:
        # find the elements on the page
        elements = self.selenium.find_elements(By.CSS_SELECTOR, 'table#result_list > tbody > tr > th > a')
        got_result_list = [l.get_attribute('href').split('?')[0] for l in elements]

        # find the urls that are being linked to
        url = 'admin:{}_change'.format(model)
        expected_result_list = [
            self.live_server_url + self._resolve_url(url, args=(o.pk,)) for o in objects
        ]

        # check that the result list is the same
        self.assertListEqual(got_result_list, expected_result_list)

    def _assert_alumni_results(self, names: List[str]) -> None:
        """ Asserts that a given set of admin search results are showing up on the current search page """

        objects = [Alumni.objects.get(profile__username=name) for name in names]
        return self._assert_admin_results('alumni_alumni', objects)

    def _select_filter(self, name: str, title: str) -> None:

        # find the filter <ul> from the <summary>
        summary = self.selenium.find_element(By.XPATH,  '//*[@id="changelist-filter"]/details/summary[text()="By ' + name + '"]')
        ul = self.find_next_sibling(summary)
        if ul is None:
            raise AssertionError("Filter does not exist")

        # click the filter with the right title
        for a in ul.find_elements(By.CSS_SELECTOR, 'a'):
            if a.text == title:
                a.click()
                return

        raise AssertionError("Filter value does not exist")


    def test_view(self):
        ALL_ALUMNI = ['eilie', 'Ramila', 'nmal', 'yfeng', 'LiRongTsao', 'Hichat', 'Irew1996', 'Douner', 'Aint1975', 'Mounfem']

        # all the results
        self.load_live_url('admin:alumni_alumni_changelist', selector='.app-alumni.model-alumni.change-list')
        self._assert_alumni_results(ALL_ALUMNI)

        # Application approval (yes / no)
        self._select_filter('Application Approval', 'Yes')
        self._assert_alumni_results(ALL_ALUMNI)

        self._select_filter('Application Approval', 'No')
        self._assert_alumni_results([])
