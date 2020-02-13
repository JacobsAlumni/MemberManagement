from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

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
        self.submit_form('edit_skills', 'input_id_submit')

        # check that nothing happened
        self.assertEqual(self.current_url, reverse('edit_skills'),
                         'Check that we stayed on the right page')

        # check that everything stayed the same
        self.assertEqual(self.obj.skills.otherDegrees,
                         "Bachelor of Computer Science from IUB")
        self.assertEqual(self.obj.skills.spokenLanguages,
                         "German, English, Spanish")
        self.assertEqual(self.obj.skills.programmingLanguages,
                         "HTML, CSS, JavaScript, Python")
        self.assertEqual(self.obj.skills.areasOfInterest,
                         "Start-Ups, Surfing, Big Data, Human Rights")
        self.assertEqual(self.obj.skills.alumniMentor, False)

    def test_edit_complete(self):
        # enter nothing
        self.submit_form('edit_skills', 'input_id_submit', send_form_keys={
            'id_otherDegrees': 'Fancy Degree from FancyU',
            'id_spokenLanguages': 'English, German, Spanish',
            'id_programmingLanguages': 'CSS, HTML, JavaScript, Python',
            'id_areasOfInterest': 'Nothing at all'
        }, select_checkboxes={
            'id_alumniMentor': True,
        })

        # check that nothing happened
        self.assertEqual(self.current_url, reverse('edit_skills'),
                         'Check that we stayed on the right page')

        # check that everything saved
        self.assertEqual(self.obj.skills.otherDegrees,
                         "Fancy Degree from FancyU")
        self.assertEqual(self.obj.skills.spokenLanguages,
                         "English, German, Spanish")
        self.assertEqual(self.obj.skills.programmingLanguages,
                         "CSS, HTML, JavaScript, Python")
        self.assertEqual(self.obj.skills.areasOfInterest, "Nothing at all")
        self.assertEqual(self.obj.skills.alumniMentor, True)

    def test_edit_empty(self):
        # enter nothing
        self.submit_form('edit_skills', 'input_id_submit', send_form_keys={
            'id_otherDegrees': '',
            'id_spokenLanguages': '',
            'id_programmingLanguages': '',
            'id_areasOfInterest': ''
        }, select_checkboxes={
            'id_alumniMentor': False,
        })

        # check that nothing happened
        self.assertEqual(self.current_url, reverse('edit_skills'),
                         'Check that we stayed on the right page')

        # check that everything saved
        self.assertEqual(self.obj.skills.otherDegrees, '')
        self.assertEqual(self.obj.skills.spokenLanguages, '')
        self.assertEqual(self.obj.skills.programmingLanguages, '')
        self.assertEqual(self.obj.skills.areasOfInterest, '')
        self.assertEqual(self.obj.skills.alumniMentor, False)
