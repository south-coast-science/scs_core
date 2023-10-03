"""
Created on 24 May 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
{"key-id": "ABC", "secret-key": "123"}
"""

import json
import requests

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.client.api_client import APIClient


# --------------------------------------------------------------------------------------------------------------------

class AccessKeyManager(APIClient):
    """
    classdocs
    """

    __URL = "https://a0vjvahph1.execute-api.us-west-2.amazonaws.com/default/CognitoDeviceKey"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def get(self, token):
        response = requests.get(self.__URL, headers=self._token_headers(token))
        self._check_response(response)

        for id, secret in json.loads(response.json()).items():
            return AccessKey(id, secret)                                # only one key
