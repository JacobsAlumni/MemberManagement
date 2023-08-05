from __future__ import annotations

from unittest import mock

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from datetime import timezone, datetime

from MemberManagement.tests.integration import IntegrationTest

MOCKED_TIME = datetime(
    2019, 9, 19, 16, 42, 5, 269, tzinfo=timezone.utc)


class FinalizeTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/signup_07a_starter.json']
    user = 'Mounfem'

    @mock.patch('django.utils.timezone.now', mock.Mock(return_value=MOCKED_TIME))
    def test_setup_finalize(self) -> None:
        self.submit_form('setup_setup', 'input_id_submit')

        self.assert_url_equal('portal',
                              'Check that the user gets redirected to the portal page')

        setup = self.user.alumni.setup
        self.assertEqual(setup.date, MOCKED_TIME)
