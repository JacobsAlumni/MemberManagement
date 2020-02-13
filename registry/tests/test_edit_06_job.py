from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from alumni.fields.industry import IndustryField
from alumni.fields.job import JobField
from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest


class EditJobTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')
        self.obj = Alumni.objects.get(profile__username='Mounfem')

    def test_noedit(self):
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('edit_job', 'input_id_submit')

        # check that nothing happened
        self.assertEqual(self.current_url, reverse('edit_job'),
                         'Check that we stayed on the right page')

        # check that everything stayed the same
        self.assertEqual(self.obj.job.employer, "Solution Realty")
        self.assertEqual(self.obj.job.position, "Junior Research Engineer")
        self.assertEqual(self.obj.job.industry, IndustryField.NANOTECHNOLOGY)
        self.assertEqual(self.obj.job.job, JobField.SOFTWARE_DEVELOPMENT_IT)

    def test_edit_complete(self):
        # enter nothing
        self.submit_form('edit_job', 'input_id_submit', send_form_keys={
            'id_employer': 'Problem Dream',
            'id_position': 'Senior Production Consultant',
        }, select_dropdowns={
            'id_industry': 'Military',
            'id_job': 'Retail',
        })

        # check that nothing happened
        self.assertEqual(self.current_url, reverse('edit_job'),
                         'Check that we stayed on the right page')

        # check that everything saved
        self.assertEqual(self.obj.job.employer, "Problem Dream")
        self.assertEqual(self.obj.job.position, "Senior Production Consultant")
        self.assertEqual(self.obj.job.industry, IndustryField.MILITARY)
        self.assertEqual(self.obj.job.job, JobField.RETAIL)

    def test_edit_empty(self):
        # enter nothing
        self.submit_form('edit_job', 'input_id_submit', send_form_keys={
            'id_employer': '',
            'id_position': '',
        }, select_dropdowns={
            'id_industry': 'Other',
            'id_job': 'Other',
        })

        # check that nothing happened
        self.assertEqual(self.current_url, reverse('edit_job'),
                         'Check that we stayed on the right page')

        # check that everything saved
        self.assertEqual(self.obj.job.employer, None)
        self.assertEqual(self.obj.job.position, None)
        self.assertEqual(self.obj.job.industry, IndustryField.OTHER)
        self.assertEqual(self.obj.job.job, JobField.OTHER)
