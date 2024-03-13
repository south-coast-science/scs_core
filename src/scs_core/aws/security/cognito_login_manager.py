"""
Created on 23 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.security.cognito_authentication import AuthenticationResult


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('CogSecAPI/CognitoLogin',
                   'https://lnh2y9ip75.execute-api.us-west-2.amazonaws.com/default/CognitoLogin')


# --------------------------------------------------------------------------------------------------------------------

class CognitoLoginManager(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def user_login(self, credentials):
        url = Endpoint.url('user')
        headers = self._auth_headers()

        response = requests.post(url, headers=headers, json=credentials.as_json())
        self._check_response(response)

        return AuthenticationResult.construct_from_res(response)


    def device_login(self, credentials):
        url = Endpoint.url('device')
        headers = self._auth_headers()

        response = requests.post(url, headers=headers, json=credentials.as_json())
        self._check_response(response)

        return AuthenticationResult.construct_from_res(response)
