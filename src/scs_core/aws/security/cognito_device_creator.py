"""
Created on 24 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Enables a device to register itself as a CognitoDevice
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.security.cognito_device import CognitoDeviceIdentity

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('CogDevCreAPI/CognitoDeviceCreator',
                   'https://bf32xbgymi.execute-api.us-west-2.amazonaws.com/default/CognitoDeviceCreator')


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceCreator(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def may_create(self, device_tag):
        params = {"DeviceTag": device_tag}

        response = requests.get(Endpoint.url(), headers=self._auth_headers(), params=params)
        self._check_response(response)

        return response.json()


    def create(self, identity: CognitoDeviceIdentity):
        response = requests.post(Endpoint.url(), headers=self._auth_headers(), data=JSONify.dumps(identity))
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())
