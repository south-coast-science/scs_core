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
from scs_core.aws.config.endpoint import APIEndpoint


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('CogDevKeyAPI/CognitoDeviceKey',
                   'https://a0vjvahph1.execute-api.us-west-2.amazonaws.com/default/CognitoDeviceKey')


# --------------------------------------------------------------------------------------------------------------------

class AccessKeyManager(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def get(self, token):
        response = requests.get(Endpoint.url(), headers=self._token_headers(token))
        self._check_response(response)

        for id, secret in json.loads(response.json()).items():
            return AccessKey(id, secret)                                # only one key
