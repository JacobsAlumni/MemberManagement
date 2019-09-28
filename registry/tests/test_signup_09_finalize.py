from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from MemberManagement.tests.integration import IntegrationTest

from django.utils import timezone

from unittest import mock

from alumni.models import Alumni

MOCKED_TIME = timezone.datetime(2019, 9, 19, 16, 42, 5, 269, tzinfo=timezone.utc)


class FinalizeTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_07a_starter.json']

    def setUp(self):
        super().setUp()
        self.login('Mounfem')

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_setup_finalize(self):
        self.submit_form('/portal/setup/completed/', 'input_id_submit')

        self.assertEqual(self.current_url, '/portal/',
                         'Check that the user gets redirected to the portal page')

        obj = Alumni.objects.first().setup
        self.assertEqual(obj.date,
                         MOCKED_TIME)
