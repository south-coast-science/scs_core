"""
Created on 5 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.security.cognito_device import CognitoDeviceIdentity
from scs_core.aws.security.cognito_device_manager import Endpoint


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceFinder(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self, token):
        url = Endpoint.url('retrieve', 'all')

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoDeviceIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_tag(self, token, tag):
        url = Endpoint.url('retrieve', 'in')
        params = {"username": tag}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return tuple(CognitoDeviceIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def get_by_tag(self, token, tag):
        url = Endpoint.url('retrieve', 'exact')
        params = {"username": tag}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceIntrospector(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find_self(self, token):
        url = Endpoint.url('self')

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())
