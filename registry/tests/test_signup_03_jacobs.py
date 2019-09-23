from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest

from alumni.models import Alumni
from alumni.fields.college import CollegeField
from alumni.fields.degree import DegreeField
from alumni.fields.major import MajorField
from alumni.fields.year import ClassField


class SocialTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_02_social.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')

    def test_signup_jacobs_complete(self):
        self.submit_form('/portal/setup/jacobs/', 'input_id_submit', send_form_keys={
            'id_comments': 'I am not real',
        }, select_dropdowns={
            'id_college': 'Nordmetall',
            'id_degree': 'Bachelor of Science',
            'id_graduation': 'Class of 2011',
            'id_major': 'Physics',
        })

        self.assertEqual(self.current_url, '/portal/setup/job/',
                         'Check that the user gets redirected to the job page')

        obj = Alumni.objects.first().jacobs
        self.assertEqual(obj.college, CollegeField.NORDMETALL)
        self.assertEqual(obj.degree, DegreeField.BACHELOR_SCIENCE)
        self.assertEqual(obj.graduation, ClassField.C_2011)
        self.assertEqual(obj.major, MajorField.PHYSICS)
        self.assertEqual(obj.comments, 'I am not real')

    def test_signup_jacobs_empty(self):
        self.submit_form('/portal/setup/jacobs/', 'input_id_submit', send_form_keys={
            'id_comments': '',
        }, select_dropdowns={
            'id_college': None,
            'id_degree': None,
            'id_graduation': 'Other (Please specify in comments)',
            'id_major': 'Other (Please specify in comments)',
        })

        self.assertEqual(self.current_url, '/portal/setup/job/',
                         'Check that the user gets redirected to the job page')

        obj = Alumni.objects.first().jacobs
        self.assertEqual(obj.college, None)
        self.assertEqual(obj.degree, None)
        self.assertEqual(obj.graduation, ClassField.OTHER)
        self.assertEqual(obj.major, MajorField.OTHER)
        self.assertEqual(obj.comments, '')
