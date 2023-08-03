"""
Created on 22 May 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"device_tag": "scs-ap1-303"}
"""

import requests

from scs_core.aws.client.api_client import APIClient

from scs_core.data.json import JSONable, JSONify


# --------------------------------------------------------------------------------------------------------------------

class DeviceWhitelistManager(APIClient):
    """
    classdocs
    """

    __URL = 'https://i8lwsjuksc.execute-api.us-west-2.amazonaws.com/default/DeviceWhitelist'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self, token):
        response = requests.get(self.__URL, headers=self._token_headers(token))
        self._check_response(response)

        return sorted([DeviceWhitelistItem.construct_from_jdict(jdict) for jdict in response.json()])


    def create(self, token, device_tag):
        payload = DeviceWhitelistItem(device_tag)

        response = requests.post(self.__URL, headers=self._token_headers(token), data=JSONify.dumps(payload))
        self._check_response(response)


    def delete(self, token, device_tag):
        payload = DeviceWhitelistItem(device_tag)

        response = requests.delete(self.__URL, headers=self._token_headers(token), data=JSONify.dumps(payload))
        self._check_response(response)


# --------------------------------------------------------------------------------------------------------------------

class DeviceWhitelistItem(JSONable):
    """
    classdocs
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device_tag = jdict.get('device-tag')

        return cls(device_tag)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_tag):
        """
        Constructor
        """
        self.__device_tag = device_tag                              # string


    def __lt__(self, other):
        return self.device_tag < other.device_tag


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return {'device-tag': self.device_tag}


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device_tag(self):
        return self.__device_tag


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceWhitelistItem:{device_tag:%s}" % self.device_tag
