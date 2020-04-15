from __future__ import annotations

from django_selenium_test import IntegrationTest as IntegrationTestI, IntegrationTestBase as IntegrationTestBaseI
from django.core.management import call_command

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Type, Any, List, Dict, Union, IO
    from django.contrib.auth.models import User
    from django_selenium_clean import SeleniumWrapper
    from selenium.webdriver.remote.webelement import WebElement

class CustomIntegrationTestMixin():
    find_element_selector = '.main-container'
    def load_fixture(self, path: str) -> None:
        """ Loads a fixture for use in unit tests """

        call_command('loaddata', path)

class IntegrationTestBase(CustomIntegrationTestMixin, IntegrationTestBaseI):
    pass

class IntegrationTest(CustomIntegrationTestMixin, IntegrationTestI):
    pass
