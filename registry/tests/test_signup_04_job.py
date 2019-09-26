from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest

from alumni.models import Alumni
from alumni.fields.industry import IndustryField
from alumni.fields.job import JobField


class JobTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_03_jacobs.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')

    def test_signup_job_complete(self):
        self.submit_form('/portal/setup/job/', 'input_id_submit', send_form_keys={
            'id_employer': 'Solution Realty',
            'id_position': 'Junior Research Engineer',
        }, select_dropdowns={
            'id_industry': 'Nanotechnology',
            'id_job': 'Software Development / IT',
        })

        self.assertEqual(self.current_url, '/portal/setup/skills/',
                         'Check that the user gets redirected to the skills page')

        obj = Alumni.objects.first().job
        self.assertEqual(obj.employer, "Solution Realty")
        self.assertEqual(obj.position, "Junior Research Engineer")
        self.assertEqual(obj.industry, IndustryField.NANOTECHNOLOGY)
        self.assertEqual(obj.job, JobField.SOFTWARE_DEVELOPMENT_IT)

    def test_signup_job_empty(self):
        self.submit_form('/portal/setup/job/', 'input_id_submit', send_form_keys={
            'id_employer': '',
            'id_position': '',
        }, select_dropdowns={
            'id_industry': 'Other',
            'id_job': 'Other',
        })

        self.assertEqual(self.current_url, '/portal/setup/skills/',
                         'Check that the user gets redirected to the job page')

        obj = Alumni.objects.first().job
        self.assertEqual(obj.employer, None)
        self.assertEqual(obj.position, None)
        self.assertEqual(obj.industry, IndustryField.OTHER)
        self.assertEqual(obj.job, JobField.OTHER)
