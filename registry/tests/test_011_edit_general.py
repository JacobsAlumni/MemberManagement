from __future__ import annotations

import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from alumni.fields.category import AlumniCategoryField
from alumni.fields.gender import GenderField
from MemberManagement.tests.integration import IntegrationTest

from selenium.webdriver.common.by import By


class EditDataTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ["registry/tests/fixtures/integration.json"]
    user = "Mounfem"

    def test_noedit(self) -> None:
        """Tests that entering nothing doesn't change anything"""

        # enter nothing
        self.submit_form("edit", "input_id_submit")
        self.assert_url_equal("edit")

        alumni = self.user.alumni
        alumni.refresh_from_db()

        # check that everything stayed the same
        self.assertEqual(alumni.profile.username, "Mounfem")
        self.assertEqual(alumni.givenName, "Anna")
        self.assertEqual(alumni.middleName, None)
        self.assertEqual(alumni.familyName, "Freytag")
        self.assertEqual(alumni.email, "AnnaFreytag@dayrep.com")
        self.assertEqual(alumni.existingEmail, None)
        self.assertEqual(alumni.resetExistingEmailPassword, False)
        self.assertEqual(alumni.sex, GenderField.FEMALE)
        self.assertEqual(alumni.birthday, datetime.date(1948, 11, 7))
        self.assertListEqual(
            list(map(lambda c: c.name, alumni.nationality)), ["Germany"]
        )
        self.assertEqual(alumni.category, AlumniCategoryField.REGULAR)

    def test_data_regular(self) -> None:
        """Tests that all fields can be changed"""

        self.submit_form(
            "edit",
            "input_id_submit",
            send_form_keys={
                "id_givenName": "John",
                "id_middleName": "C",
                "id_familyName": "Day",
                "id_email": "JohnDay@dayrep.com",
            },
            select_dropdowns={
                "id_sex": "Male",
                "id_nationality": ("GM",),
            },
            script_value={
                "id_birthday": "1949-10-08",
            },
        )
        self.assert_url_equal("edit")

        alumni = self.user.alumni
        alumni.refresh_from_db()

        # check that the right alumni object was created
        self.assertEqual(alumni.givenName, "John")
        self.assertEqual(alumni.middleName, "C")
        self.assertEqual(alumni.familyName, "Day")
        self.assertEqual(alumni.email, "JohnDay@dayrep.com")
        self.assertEqual(alumni.existingEmail, None)
        self.assertEqual(alumni.resetExistingEmailPassword, False)
        self.assertEqual(alumni.sex, GenderField.MALE)
        self.assertEqual(alumni.birthday, datetime.date(1949, 10, 8))
        self.assertListEqual(
            list(map(lambda c: c.name, alumni.nationality)), ["Gambia"]
        )
        self.assertEqual(alumni.category, AlumniCategoryField.REGULAR)

    def test_nojacobsemail(self) -> None:
        """Tests that we can't use a jacobs email as private email"""

        # enter nothing
        self.submit_form(
            "edit",
            "input_id_submit",
            send_form_keys={
                "id_email": "AnnaFreytag@jacobs-university.de",
            },
        )

        # check that we stayed on the page, but the email field was marked incorrect
        self.assert_url_equal("edit")
        self.assertIn(
            "uk-form-danger",
            self.selenium.find_element(By.ID, "id_email")
            .get_attribute("class")
            .split(" "),
            "email field marked up as incorrect",
        )

        alumni = self.user.alumni
        alumni.refresh_from_db()

        # check that everything stayed the same
        self.assertEqual(alumni.profile.username, "Mounfem")
        self.assertEqual(alumni.givenName, "Anna")
        self.assertEqual(alumni.middleName, None)
        self.assertEqual(alumni.familyName, "Freytag")
        self.assertEqual(alumni.email, "AnnaFreytag@dayrep.com")
        self.assertEqual(alumni.existingEmail, None)
        self.assertEqual(alumni.resetExistingEmailPassword, False)
        self.assertEqual(alumni.sex, GenderField.FEMALE)
        self.assertEqual(alumni.birthday, datetime.date(1948, 11, 7))
        self.assertListEqual(
            list(map(lambda c: c.name, alumni.nationality)), ["Germany"]
        )
        self.assertEqual(alumni.category, AlumniCategoryField.REGULAR)
