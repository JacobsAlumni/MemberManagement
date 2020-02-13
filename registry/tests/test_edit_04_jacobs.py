from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from alumni.fields.college import CollegeField
from alumni.fields.degree import DegreeField
from alumni.fields.major import MajorField
from alumni.fields.year import ClassField
from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest


class EditJacobsTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')
        self.obj = Alumni.objects.get(profile__username='Mounfem')

    def test_noedit(self):
        """ Tests that entering nothing doesn't change anything """

        # enter nothing
        self.submit_form('edit_jacobs', 'input_id_submit')

        # check that nothing happened
        self.assertEqual(self.current_url, reverse('edit_jacobs'),
                         'Check that we stayed on the right page')

        # check that everything stayed the same
        self.assertEqual(self.obj.jacobs.college, CollegeField.NORDMETALL)
        self.assertEqual(self.obj.jacobs.degree, DegreeField.BACHELOR_SCIENCE)
        self.assertEqual(self.obj.jacobs.graduation, ClassField.C_2011)
        self.assertEqual(self.obj.jacobs.major, MajorField.PHYSICS)
        self.assertEqual(self.obj.jacobs.comments, 'I am not real')

    def test_edit_complete(self):
        self.submit_form('edit_jacobs', 'input_id_submit', send_form_keys={
            'id_comments': 'I am real',
        }, select_dropdowns={
            'id_college': 'College III',
            'id_degree': 'Master of Arts',
            'id_graduation': 'Class of 2012',
            'id_major': 'Humanities',
        })

        # check that we stayed on the right page
        self.assertEqual(self.current_url, reverse('edit_jacobs'),
                         'Check that we stayed on the right page')

        # check that everything stayed the same
        self.assertEqual(self.obj.jacobs.college, CollegeField.CIII)
        self.assertEqual(self.obj.jacobs.degree, DegreeField.MASTER_ARTS)
        self.assertEqual(self.obj.jacobs.graduation, ClassField.C_2012)
        self.assertEqual(self.obj.jacobs.major, MajorField.HUMANITIES)
        self.assertEqual(self.obj.jacobs.comments, 'I am real')

    def test_edit_empty(self):
        self.submit_form('edit_jacobs', 'input_id_submit', send_form_keys={
            'id_comments': '',
        }, select_dropdowns={
            'id_college': '---------',
            'id_degree': '---------',
            'id_graduation': 'Other (Please specify in comments)',
            'id_major': 'Other (Please specify in comments)',
        })

        # check that we stayed on the right page
        self.assertEqual(self.current_url, reverse('edit_jacobs'),
                         'Check that we stayed on the right page')

        # check that everything stayed the same
        self.assertEqual(self.obj.jacobs.college, None)
        self.assertEqual(self.obj.jacobs.degree, None)
        self.assertEqual(self.obj.jacobs.graduation, ClassField.OTHER)
        self.assertEqual(self.obj.jacobs.major, MajorField.OTHER)
        self.assertEqual(self.obj.jacobs.comments, '')
