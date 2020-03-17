from __future__ import annotations

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from alumni.fields.college import CollegeField
from alumni.fields.degree import DegreeField
from alumni.fields.major import MajorField
from alumni.fields.year import ClassField
from MemberManagement.tests.integration import IntegrationTest


class EditJacobsTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Mounfem'

    def test_noedit(self) -> None:
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('edit_jacobs', 'input_id_submit')
        self.assert_url_equal('edit_jacobs')

        # check that everything stayed the same
        jacobs = self.user.alumni.jacobs
        self.assertEqual(jacobs.college, CollegeField.NORDMETALL)
        self.assertEqual(jacobs.degree, DegreeField.BACHELOR_SCIENCE)
        self.assertEqual(jacobs.graduation, ClassField.C_2011)
        self.assertEqual(jacobs.major, MajorField.PHYSICS)
        self.assertEqual(jacobs.comments, 'I am not real')

    def test_edit_complete(self) -> None:
        self.submit_form('edit_jacobs', 'input_id_submit', send_form_keys={
            'id_comments': 'I am real',
        }, select_dropdowns={
            'id_college': 'College III',
            'id_degree': 'Master of Arts',
            'id_graduation': 'Class of 2012',
            'id_major': 'Humanities',
        })
        self.assert_url_equal('edit_jacobs')

        # check that everything stayed the same
        jacobs = self.user.alumni.jacobs
        self.assertEqual(jacobs.college, CollegeField.CIII)
        self.assertEqual(jacobs.degree, DegreeField.MASTER_ARTS)
        self.assertEqual(jacobs.graduation, ClassField.C_2012)
        self.assertEqual(jacobs.major, MajorField.HUMANITIES)
        self.assertEqual(jacobs.comments, 'I am real')

    def test_edit_empty(self) -> None:
        self.submit_form('edit_jacobs', 'input_id_submit', send_form_keys={
            'id_comments': '',
        }, select_dropdowns={
            'id_college': '---------',
            'id_degree': '---------',
            'id_graduation': 'Other (Please specify in comments)',
            'id_major': 'Other (Please specify in comments)',
        })
        self.assert_url_equal('edit_jacobs')

        # check that everything stayed the same
        jacobs = self.user.alumni.jacobs
        self.assertEqual(jacobs.college, None)
        self.assertEqual(jacobs.degree, None)
        self.assertEqual(jacobs.graduation, ClassField.OTHER)
        self.assertEqual(jacobs.major, MajorField.OTHER)
        self.assertEqual(jacobs.comments, '')
