from __future__ import annotations

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from MemberManagement.tests.integration import IntegrationTest

from ..models import VoteLink, VoteToken
from alumni.models import Alumni


class VoteLinkTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = [
        'registry/tests/fixtures/integration.json',
        'registry/tests/fixtures/votelinks.json',
    ]

    def test_create_tokens(self) -> None:
        """ Tests that voting tokens are created """

        # get the link and user object
        link = VoteLink.objects.get(pk=1)
        alumni = Alumni.objects.get(profile__username='Mounfem')

        # check that there aren't any vote tokens right now
        self.assertEqual(link.votetoken_set.count(), 0)

        # make a token
        token = link.get_token(alumni)
        self.assertIsNotNone(
            token, 'check that get_token returns a token object')
        self.assertEqual(token.alumni, alumni)
        self.assertEqual(token.vote, link)

        # check that the token was made
        self.assertEqual(link.votetoken_set.count(), 1)
        self.assertEqual(VoteToken.objects.first(), token)

        # grab the token again
        self.assertEqual(link.get_token(
            alumni), token, 'Check that getting the token again returns the same token')

    def test_export_tokens(self) -> None:
        """ Tests that exporting tokens works as expected """

        # get the link and user object
        link = VoteLink.objects.get(pk=1)

        # create tokens for all the alumni and count them
        tokens = []
        for alumni in Alumni.objects.all():
            token = link.get_token(alumni)
            tokens.append(str(token.token))
        tokens = sorted(tokens)
        expect_tokens = '\r\n'.join(tokens + ['']).encode('utf-8')

        # Check that the superuser can download tokens
        self.login('Mounfem')
        tokens_download_ok, got_tokens = self.get_url_download(
            'registry_tokens', kwargs={'id': '1'})
        self.assertTrue(tokens_download_ok,
                        "Tokens could be downloaded successfully")
        self.assertEqual(got_tokens, expect_tokens,
                         "Right tokens were returned")

        # Check that the non-superuser can not download tokens
        self.load_live_url('logout')
        self.login('Aint1975')
        _, got_tokens = self.get_url_download(
            'registry_tokens', kwargs={'id': '1'})
        self.assertNotEqual(got_tokens, expect_tokens,
                            "Non-superuser can not download tokens")

    def test_show_tokens_approved(self) -> None:

        # login and load the voting page
        self.login('Mounfem')
        self.load_live_url('registry_vote')

        # load the token ids that were generated
        Mounfem = Alumni.objects.get(profile__username='Mounfem')
        Active_Token = str(VoteLink.objects.get(pk=1).get_token(Mounfem).token)
        Active_Without_Token = str(
            VoteLink.objects.get(pk=2).get_token(Mounfem).token)

        # check the first link
        vote_link = self.find_element('#id_vote_link_1')
        self.assertEqual(vote_link.get_attribute('href'), 'https://example.com/active-token/?token={}'.format(
            Active_Token), 'Check that the first link is set correctly')
        self.assert_element_exists(
            '#id_vote_link_1_personalized', 'Check that the first link is marked as personalized')
        vote_token = self.find_element('#id_vote_token_1')
        self.assertEqual(vote_token.get_attribute(
            'value'), Active_Token, 'Check that the first token is set correctly')

        # check the second link
        vote_link = self.find_element('#id_vote_link_2')
        self.assertEqual(vote_link.get_attribute(
            'href'), 'https://example.com/active-no-token/', 'Check that the second link is set correctly')
        self.assert_element_not_exists(
            '#id_vote_link_2_personalized', 'Check that the second link is not marked as personalized')
        vote_token = self.find_element('#id_vote_token_2')
        self.assertEqual(vote_token.get_attribute(
            'value'), Active_Without_Token, 'Check that the second token is set correctly')

        # check that no third link exists
        self.assert_element_not_exists('#id_vote_link_3')
        self.assert_element_not_exists('#id_vote_link_3_personalized')
        self.assert_element_not_exists('#id_vote_token_3')

    def test_show_tokens_unapproved(self) -> None:
        Mounfem = Alumni.objects.get(profile__username='Mounfem')
        Mounfem.approval.approval = False
        Mounfem.approval.save()

        self.login('Mounfem')
        self.load_live_url('registry_vote')

        # check that no links exist
        self.assert_element_not_exists('#id_vote_link_1')
        self.assert_element_not_exists('#id_vote_link_1_personalized')
        self.assert_element_not_exists('#id_vote_token_1')

        self.assert_element_not_exists('#id_vote_link_2')
        self.assert_element_not_exists('#id_vote_link_2_personalized')
        self.assert_element_not_exists('#id_vote_token_2')

        self.assert_element_not_exists('#id_vote_link_3')
        self.assert_element_not_exists('#id_vote_link_3_personalized')
        self.assert_element_not_exists('#id_vote_token_3')

        # check that no tokens were created
        self.assertEqual(VoteToken.objects.count(), 0, 'check that no tokens were created')
