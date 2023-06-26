"""
Created on 5 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.security.cognito_device import CognitoDeviceIdentity

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceManager(APIClient):
    """
    classdocs
    """

    __URL = 'https://6c2sfqt656.execute-api.us-west-2.amazonaws.com/default/CognitoDevices'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, token, identity):
        response = self._http_client.post(self.__URL, headers=self._token_headers(token), data=JSONify.dumps(identity))
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())


    def update(self, token, identity):
        response = self._http_client.patch(self.__URL, headers=self._token_headers(token), data=JSONify.dumps(identity))
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())



    def delete(self, token, device_tag):
        payload = {"DeviceTag": device_tag}

        response = self._http_client.delete(self.__URL, headers=self._token_headers(token), data=JSONify.dumps(payload))
        self._check_response(response)

        # TODO: delete device from organisations?


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceManager:{}"
