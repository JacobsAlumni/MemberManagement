from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from alumni.fields.industry import IndustryField
from alumni.fields.job import JobField
from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest


class EditJobTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Mounfem'

    def test_noedit(self):
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('edit_job', 'input_id_submit')
        self.assert_url_equal('edit_job')

        # check that everything stayed the same
        job = self.user.alumni.job
        self.assertEqual(job.employer, "Solution Realty")
        self.assertEqual(job.position, "Junior Research Engineer")
        self.assertEqual(job.industry, IndustryField.NANOTECHNOLOGY)
        self.assertEqual(job.job, JobField.SOFTWARE_DEVELOPMENT_IT)

    def test_edit_complete(self):
        # enter nothing
        self.submit_form('edit_job', 'input_id_submit', send_form_keys={
            'id_employer': 'Problem Dream',
            'id_position': 'Senior Production Consultant',
        }, select_dropdowns={
            'id_industry': 'Military',
            'id_job': 'Retail',
        })
        self.assert_url_equal('edit_job')

        # check that everything saved
        job = self.user.alumni.job
        self.assertEqual(job.employer, "Problem Dream")
        self.assertEqual(job.position, "Senior Production Consultant")
        self.assertEqual(job.industry, IndustryField.MILITARY)
        self.assertEqual(job.job, JobField.RETAIL)

    def test_edit_empty(self):
        # enter nothing
        self.submit_form('edit_job', 'input_id_submit', send_form_keys={
            'id_employer': '',
            'id_position': '',
        }, select_dropdowns={
            'id_industry': 'Other',
            'id_job': 'Other',
        })
        self.assert_url_equal('edit_job')

        # check that everything saved
        job = self.user.alumni.job
        self.assertEqual(job.employer, None)
        self.assertEqual(job.position, None)
        self.assertEqual(job.industry, IndustryField.OTHER)
        self.assertEqual(job.job, JobField.OTHER)
