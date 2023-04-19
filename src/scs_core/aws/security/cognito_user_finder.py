"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.security.cognito_user import CognitoUserIdentity

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserFinder(APIClient):
    """
    classdocs
    """

    __URL = 'https://iw0jza59y1.execute-api.us-west-2.amazonaws.com/default/CognitoUsersFinder/'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self, token):
        url = '/'.join((self.__URL, 'all'))

        response = self._http_client.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_status(self, token, confirmation_status):
        url = '/'.join((self.__URL, confirmation_status.lower()))

        response = self._http_client.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_enabled(self, token, enabled):
        url = '/'.join((self.__URL, 'enabled' if enabled else 'disabled'))

        response = self._http_client.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_email(self, token, email):
        url = '/'.join((self.__URL, 'in'))
        payload = JSONify.dumps({"Email": email})

        response = self._http_client.get(url, data=payload, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_usernames(self, token, usernames):
        url = '/'.join((self.__URL, 'usernames'))
        payload = JSONify.dumps(usernames)

        response = self._http_client.get(url, data=payload, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def get_by_email(self, token, email):
        url = '/'.join((self.__URL, 'exact'))
        payload = JSONify.dumps({"Email": email})

        response = self._http_client.get(url, data=payload, headers=self._token_headers(token))
        self._check_response(response)

        return CognitoUserIdentity.construct_from_jdict(response.json())


    def get_self(self, token):
        url = '/'.join((self.__URL, 'self'))

        response = self._http_client.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return CognitoUserIdentity.construct_from_jdict(response.json())
