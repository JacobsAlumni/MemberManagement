from __future__ import annotations

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest

from alumni.fields.industry import IndustryField
from alumni.fields.job import JobField


class JobTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ["registry/tests/fixtures/signup_03_jacobs.json"]
    user = "Mounfem"

    def test_signup_job_complete(self) -> None:
        self.submit_form(
            "setup_job",
            "input_id_submit",
            send_form_keys={
                "id_employer": "Solution Realty",
                "id_position": "Junior Research Engineer",
            },
            select_dropdowns={
                "id_industry": "Nanotechnology",
                "id_job": "Software Development / IT",
            },
        )

        self.assert_url_equal(
            "setup_skills", "Check that the user gets redirected to the skills page"
        )

        job = self.user.alumni.job
        self.assertEqual(job.employer, "Solution Realty")
        self.assertEqual(job.position, "Junior Research Engineer")
        self.assertEqual(job.industry, IndustryField.NANOTECHNOLOGY)
        self.assertEqual(job.job, JobField.SOFTWARE_DEVELOPMENT_IT)

    def test_signup_job_empty(self) -> None:
        self.submit_form(
            "setup_job",
            "input_id_submit",
            send_form_keys={
                "id_employer": "",
                "id_position": "",
            },
            select_dropdowns={
                "id_industry": "Other",
                "id_job": "Other",
            },
        )

        self.assert_url_equal(
            "setup_skills", "Check that the user gets redirected to the job page"
        )

        job = self.user.alumni.job
        self.assertEqual(job.employer, None)
        self.assertEqual(job.position, None)
        self.assertEqual(job.industry, IndustryField.OTHER)
        self.assertEqual(job.job, JobField.OTHER)
