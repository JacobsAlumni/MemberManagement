from __future__ import annotations

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from MemberManagement.tests.integration import IntegrationTest


class EditJobTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ["registry/tests/fixtures/integration.json"]
    user = "Mounfem"

    def test_noedit(self) -> None:
        """Tests that entering nothing doesn't change anything"""

        # enter nothing
        self.submit_form("edit_skills", "input_id_submit")
        self.assert_url_equal("edit_skills")

        # check that everything stayed the same
        skills = self.user.alumni.skills
        self.assertEqual(skills.otherDegrees, "Bachelor of Computer Science from IUB")
        self.assertEqual(skills.spokenLanguages, "German, English, Spanish")
        self.assertEqual(skills.programmingLanguages, "HTML, CSS, JavaScript, Python")
        self.assertEqual(
            skills.areasOfInterest, "Start-Ups, Surfing, Big Data, Human Rights"
        )
        self.assertEqual(skills.alumniMentor, False)

    def test_edit_complete(self) -> None:
        # enter nothing
        self.submit_form(
            "edit_skills",
            "input_id_submit",
            send_form_keys={
                "id_otherDegrees": "Fancy Degree from FancyU",
                "id_spokenLanguages": "English, German, Spanish",
                "id_programmingLanguages": "CSS, HTML, JavaScript, Python",
                "id_areasOfInterest": "Nothing at all",
            },
            select_checkboxes={
                "id_alumniMentor": True,
            },
        )
        self.assert_url_equal("edit_skills")

        # check that everything saved
        skills = self.user.alumni.skills
        self.assertEqual(skills.otherDegrees, "Fancy Degree from FancyU")
        self.assertEqual(skills.spokenLanguages, "English, German, Spanish")
        self.assertEqual(skills.programmingLanguages, "CSS, HTML, JavaScript, Python")
        self.assertEqual(skills.areasOfInterest, "Nothing at all")
        self.assertEqual(skills.alumniMentor, True)

    def test_edit_empty(self) -> None:
        # enter nothing
        self.submit_form(
            "edit_skills",
            "input_id_submit",
            send_form_keys={
                "id_otherDegrees": "",
                "id_spokenLanguages": "",
                "id_programmingLanguages": "",
                "id_areasOfInterest": "",
            },
            select_checkboxes={
                "id_alumniMentor": False,
            },
        )
        self.assert_url_equal("edit_skills")

        # check that everything saved
        skills = self.user.alumni.skills
        self.assertEqual(skills.otherDegrees, "")
        self.assertEqual(skills.spokenLanguages, "")
        self.assertEqual(skills.programmingLanguages, "")
        self.assertEqual(skills.areasOfInterest, "")
        self.assertEqual(skills.alumniMentor, False)
