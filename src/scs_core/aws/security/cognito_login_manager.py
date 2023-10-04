"""
Created on 23 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.security.cognito_authentication import AuthenticationResult


# --------------------------------------------------------------------------------------------------------------------

class CognitoLoginManager(APIClient):
    """
    classdocs
    """

    __URL = 'https://lnh2y9ip75.execute-api.us-west-2.amazonaws.com/default/CognitoLogin'
    __AUTH = '@southcoastscience.com'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def user_login(self, credentials):
        url = '/'.join((self.__URL, 'user'))
        headers = self._auth_headers(self.__AUTH)

        response = requests.post(url, headers=headers, json=credentials.as_json())
        self._check_response(response)

        return AuthenticationResult.construct_from_res(response)


    def device_login(self, credentials):
        url = '/'.join((self.__URL, 'device'))
        headers = self._auth_headers(self.__AUTH)

        response = requests.post(url, headers=headers, json=credentials.as_json())
        self._check_response(response)

        return AuthenticationResult.construct_from_res(response)
