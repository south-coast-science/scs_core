"""
Created on 22 May 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client.api_client import APIClient

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class DeviceWhitelistManager(APIClient):
    """
    classdocs
    """

    __URL = 'https://6c2sfqt656.execute-api.us-west-2.amazonaws.com/default/DeviceWhitelist'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        super().__init__(http_client)


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self, token):
        response = self._http_client.get(self.__URL, headers=self._token_headers(token))
        self._check_response(response)

        return response.json()


    def create(self, device_tag, token):
        response = self._http_client.post(self.__URL, headers=self._token_headers(token),
                                          data=JSONify.dumps(device_tag))
        self._check_response(response)


    def delete(self, device_tag, token):
        response = self._http_client.delete(self.__URL, headers=self._token_headers(token),
                                            data=JSONify.dumps(device_tag))
        self._check_response(response)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceWhitelistManager:{}"
