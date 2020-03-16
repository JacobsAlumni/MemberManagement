from __future__ import annotations

from django.conf import settings

from google.oauth2 import service_account
import googleapiclient.discovery

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Optional
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import Resource


def make_delegated_credentials(scopes: List[str]) -> Credentials:
    """ Creates a delegated_credentials object """
    credentials = service_account.Credentials.from_service_account_file(
        settings.GSUITE_AUTH_FILE, scopes=scopes)
    delegated_credentials = credentials.with_subject(
        settings.GSUITE_ADMIN_USER)
    return delegated_credentials


def make_directory_service() -> Resource:
    """ Makes a Google API directory service """

    delegated_credentials = make_delegated_credentials(
        ['https://www.googleapis.com/auth/admin.directory.user'])
    return googleapiclient.discovery.build('admin', 'directory_v1', credentials=delegated_credentials)


def get_user_id(username: str, service: Optional[Resource]=None) -> Optional[str]:
    """ Gets the gsuite user id of a given user """

    if service is None:
        service = make_directory_service()

    try:
        result = service.users().get(userKey=username, projection='basic').execute()
    except googleapiclient.errors.HttpError:
        return None

    return result['id']


def create_user(givenName: str, familyName: str, email: str, password: str, service: Optional[Resource]=None) -> str:
    """ Creates a user with the given username and password """

    if service is None:
        service = make_directory_service()

    userInfo = {
        'orgUnitPath': settings.GSUITE_ORG_PATH,
        'primaryEmail': email,
        'name': {
            'givenName': givenName,
            'familyName': familyName,
        },
        'password': password,
        'changePasswordAtNextLogin': True,
    }

    result = service.users().insert(body=userInfo).execute()
    return result['id']


def patch_user(username: str, password: Optional[str]=None, service: Optional[Resource]=None) -> str:
    """ Patches a (potentially suspended) user to have the password and be in the right organization """

    if service is None:
        service = make_directory_service()

    userPatch = {
        'orgUnitPath': settings.GSUITE_ORG_PATH,
        'suspended': False,
    }

    if password is not None:
        userPatch['password'] = password
        userPatch['changePasswordAtNextLogin'] = True

    result = service.users().patch(userKey=username, body=userPatch).execute()
    return result['id']
