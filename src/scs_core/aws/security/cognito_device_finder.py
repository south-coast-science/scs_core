"""
Created on 5 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.security.cognito_device import CognitoDeviceIdentity


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceFinder(APIClient):
    """
    classdocs
    """

    __URL = 'https://6c2sfqt656.execute-api.us-west-2.amazonaws.com/default/CognitoDevices/retrieve'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self, token):
        url = '/'.join((self.__URL, 'all'))

        response = self._http_client.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoDeviceIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def find_by_tag(self, token, tag):
        url = '/'.join((self.__URL, 'in'))
        payload = json.dumps({"username": tag})

        response = self._http_client.get(url, data=payload, headers=self._token_headers(token))
        self._check_response(response)

        return tuple(CognitoDeviceIdentity.construct_from_jdict(jdict) for jdict in response.json())


    def get_by_tag(self, token, tag):
        url = '/'.join((self.__URL, 'exact'))
        payload = json.dumps({"username": tag})

        response = self._http_client.get(url, data=payload, headers=self._token_headers(token))
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceFinder:{}"


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceIntrospector(APIClient):
    """
    classdocs
    """

    __URL = 'https://6c2sfqt656.execute-api.us-west-2.amazonaws.com/default/CognitoDevices/self'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def find_self(self, token):
        response = self._http_client.get(self.__URL, headers=self._token_headers(token))
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceIntrospector:{}"
