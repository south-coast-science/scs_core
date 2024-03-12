"""
Created on 26 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint

from scs_core.aws.manager.configuration.configuration_check_requester_intercourse import \
    ConfigurationCheckRequesterResponse


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('ConfReqAPI/MQTTConfigQueuer',
                   'https://5nkrlhaq69.execute-api.us-west-2.amazonaws.com/default/MQTTConfigQueuer')


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheckRequester(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def request(self, token, tag):
        params = {'tag': tag}

        response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=params)
        self._check_response(response)

        return ConfigurationCheckRequesterResponse.construct_from_jdict(response.json())
