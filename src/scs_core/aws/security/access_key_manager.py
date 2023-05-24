"""
Created on 24 May 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
"""

from scs_core.aws.client.api_client import APIClient

from scs_core.data.json import JSONable, JSONify


# --------------------------------------------------------------------------------------------------------------------

class AccessKeyManager(APIClient):
    """
    classdocs
    """
    __URL = "https://a0vjvahph1.execute-api.us-west-2.amazonaws.com/default/CognitoDeviceKey"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def get(self, token):
        response = self._http_client.get(self.__URL, headers=self._token_headers(token))
        self._check_response(response)

        return response.json()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AccessKeyManager:{}"
