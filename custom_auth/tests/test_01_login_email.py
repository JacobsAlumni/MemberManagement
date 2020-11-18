from __future__ import annotations

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from MemberManagement.tests.integration import IntegrationTest, IntegrationTestBase

from unittest import mock

from django.contrib.auth.models import User

from custom_auth.utils.auth import generate_login_token


class EmailLoginTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']

    @mock.patch('MemberManagement.mailutils.send_email', return_value=0)
    def test_nonexistent_email(self, mock: mock.Mock) -> None:
        self.submit_form('login', 'input_id_login', send_form_keys={
            'id_email': 'nonexistentemail@nonexistentdomain.com'
        })
        mock.assert_not_called()
        self.assert_url_equal('token_sent')

    @mock.patch('MemberManagement.mailutils.send_email', return_value=1)
    def test_existingemail_ok(self, mock: mock.Mock) -> None:
        self.submit_form('login', 'input_id_login', send_form_keys={
            'id_email': 'AnnaFreytag@dayrep.com'
        })
        mock.assert_called()
        self.assert_url_equal('token_sent')

    @mock.patch('MemberManagement.mailutils.send_email', return_value=0)
    def test_existingemail_fail(self, mock: mock.Mock) -> None:
        self.submit_form('login', 'input_id_login', send_form_keys={
            'id_email': 'AnnaFreytag@dayrep.com'
        })
        mock.assert_called()
        self.assert_url_equal('token_sent')

    def test_magiclogin(self):
        # generate the login token
        user = User.objects.get(username='Mounfem')
        token = generate_login_token(user)

        # go to the url
        self.load_live_url('email_login', url_get_params={
            'token': token
        }, url_reverse_get_params={
            'next': 'portal'
        })

        # wait for a second for the redirects to trigger
        import time
        time.sleep(1)

        # and check that we are now logged in
        self.load_live_url('portal')
        self.assert_url_equal('portal')
