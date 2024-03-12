"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.security.cognito_user import CognitoUserIdentity

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class CreEndpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('CogUsrCreAPI/CognitoUserAccountCreator',
                   'https://0knr39qhv7.execute-api.us-west-2.amazonaws.com/default/CognitoUserAccountCreator')


# --------------------------------------------------------------------------------------------------------------------

class AccEndpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('CogUsrAccAPI/CognitoUserAccounts',
                   'https://58vvigz8ue.execute-api.us-west-2.amazonaws.com/default/CognitoUserAccounts')


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserCreator(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, identity):
        headers = self._auth_headers()

        response = requests.post(CreEndpoint.url(), headers=headers, json=identity.as_json())
        self._check_response(response)

        return CognitoUserIdentity.construct_from_jdict(response.json())


    def confirm(self, email, confirmation_code):
        headers = self._auth_headers()
        payload = {
            'email': email,
            'confirmation': confirmation_code
        }

        response = requests.patch(CreEndpoint.url(), headers=headers, json=payload)
        self._check_response(response)


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserEditor(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def update(self, token, identity):
        url = AccEndpoint.url('edit')

        response = requests.patch(url, headers=self._token_headers(token), data=JSONify.dumps(identity))
        self._check_response(response)

        return CognitoUserIdentity.construct_from_jdict(response.json())


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserDeleter(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def delete(self, token, email):
        url = AccEndpoint.url('delete', email)

        response = requests.delete(url, headers=self._token_headers(token))
        self._check_response(response)
