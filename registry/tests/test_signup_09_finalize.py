from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone

from alumni.models import Alumni
from MemberManagement.tests.integration import IntegrationTest

MOCKED_TIME = timezone.datetime(
    2019, 9, 19, 16, 42, 5, 269, tzinfo=timezone.utc)


class FinalizeTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_07a_starter.json']
    user = 'Mounfem'

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_setup_finalize(self):
        self.submit_form('setup_setup', 'input_id_submit')

        self.assert_url_equal('portal',
                              'Check that the user gets redirected to the portal page')

        setup = self.user.alumni.setup
        self.assertEqual(setup.date, MOCKED_TIME)
