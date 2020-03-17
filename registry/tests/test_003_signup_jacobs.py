from __future__ import annotations

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from alumni.fields.college import CollegeField
from alumni.fields.degree import DegreeField
from alumni.fields.major import MajorField
from alumni.fields.year import ClassField
from MemberManagement.tests.integration import IntegrationTest


class JacobsTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_02_social.json']
    user = 'Mounfem'

    def test_signup_jacobs_complete(self) -> None:
        self.submit_form('setup_jacobs', 'input_id_submit', send_form_keys={
            'id_comments': 'I am not real',
        }, select_dropdowns={
            'id_college': 'Nordmetall',
            'id_degree': 'Bachelor of Science',
            'id_graduation': 'Class of 2011',
            'id_major': 'Physics',
        })

        self.assert_url_equal('setup_job',
                              'Check that the user gets redirected to the job page')

        jacobs = self.user.alumni.jacobs
        self.assertEqual(jacobs.college, CollegeField.NORDMETALL)
        self.assertEqual(jacobs.degree, DegreeField.BACHELOR_SCIENCE)
        self.assertEqual(jacobs.graduation, ClassField.C_2011)
        self.assertEqual(jacobs.major, MajorField.PHYSICS)
        self.assertEqual(jacobs.comments, 'I am not real')

    def test_signup_jacobs_empty(self) -> None:
        self.submit_form('setup_jacobs', 'input_id_submit', send_form_keys={
            'id_comments': '',
        }, select_dropdowns={
            'id_college': None,
            'id_degree': None,
            'id_graduation': 'Other (Please specify in comments)',
            'id_major': 'Other (Please specify in comments)',
        })

        self.assert_url_equal('setup_job',
                              'Check that the user gets redirected to the job page')

        jacobs = self.user.alumni.jacobs
        self.assertEqual(jacobs.college, None)
        self.assertEqual(jacobs.degree, None)
        self.assertEqual(jacobs.graduation, ClassField.OTHER)
        self.assertEqual(jacobs.major, MajorField.OTHER)
        self.assertEqual(jacobs.comments, '')
