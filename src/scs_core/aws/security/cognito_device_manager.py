"""
Created on 5 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
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
        return cls('CogDevAPI/CognitoDevices',
                   'https://6c2sfqt656.execute-api.us-west-2.amazonaws.com/default/CognitoDevices')


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceManager(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def update_self(self, token, credentials):
        url = Endpoint.url('self')

        response = requests.patch(url, headers=self._token_headers(token), data=JSONify.dumps(credentials))
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, token, identity):
        response = requests.post(Endpoint.url(), headers=self._token_headers(token), data=JSONify.dumps(identity))
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())


    def update(self, token, identity):
        response = requests.patch(Endpoint.url(), headers=self._token_headers(token), data=JSONify.dumps(identity))
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())


    def delete(self, token, device_tag):
        params = {"DeviceTag": device_tag}

        response = requests.delete(Endpoint.url(), headers=self._token_headers(token), params=params)
        self._check_response(response)

        # TODO: delete device from organisations?
