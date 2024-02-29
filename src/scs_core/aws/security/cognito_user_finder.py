"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.aws import AWS
from scs_core.aws.security.cognito_user import CognitoUserIdentity


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(object):

    URL = AWS.endpoint_url('CogUsrAPI/CognitoUsersFinder',
                           'https://iw0jza59y1.execute-api.us-west-2.amazonaws.com/default/CognitoUsersFinder')


# --------------------------------------------------------------------------------------------------------------------

class CognitoUserFinder(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self, token):
        url = '/'.join((Endpoint.URL, 'all'))

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_status(self, token, confirmation_status):
        url = '/'.join((Endpoint.URL, confirmation_status.lower()))

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_enabled(self, token, enabled):
        url = '/'.join((Endpoint.URL, 'enabled' if enabled else 'disabled'))

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_email(self, token, email):
        url = '/'.join((Endpoint.URL, 'in'))
        payload = {"Email": email}

        response = requests.get(url, headers=self._token_headers(token), json=payload)
        self._check_response(response)

        return tuple(CognitoUserIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def get_by_email(self, token, email):
        url = '/'.join((Endpoint.URL, 'exact'))
        payload = {"Email": email}

        print("url: %s" % url)

        response = requests.get(url, headers=self._token_headers(token), json=payload)
        self._check_response(response)

        return CognitoUserIdentity.construct_from_jdict(response.json())


    def get_self(self, token):
        url = '/'.join((Endpoint.URL, 'self'))

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return CognitoUserIdentity.construct_from_jdict(response.json())
