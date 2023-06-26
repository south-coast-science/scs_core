"""
Created on 24 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Enables a device to register itself as a CognitoDevice
"""

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.security.cognito_device import CognitoDeviceCredentials, CognitoDeviceIdentity

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class CognitoDeviceCreator(APIClient):
    """
    classdocs
    """

    __URL = 'https://bf32xbgymi.execute-api.us-west-2.amazonaws.com/default/CognitoDeviceCreator'
    __AUTH = "@southcoastscience.com"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def create(self, identity: CognitoDeviceCredentials):
        response = self._http_client.post(self.__URL, headers=self._auth_headers(self.__AUTH),
                                          data=JSONify.dumps(identity))
        self._check_response(response)

        return CognitoDeviceIdentity.construct_from_jdict(response.json())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoDeviceCreator:{}"
