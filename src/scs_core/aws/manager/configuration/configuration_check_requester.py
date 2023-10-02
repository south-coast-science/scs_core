"""
Created on 26 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.manager.configuration.configuration_check_requester_intercourse import \
    ConfigurationCheckRequesterResponse


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheckRequester(APIClient):
    """
    classdocs
    """

    __URL = "https://5nkrlhaq69.execute-api.us-west-2.amazonaws.com/default/MQTTConfigQueuer"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def request(self, token, tag):
        params = {'tag': tag}

        response = requests.get(self.__URL, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return ConfigurationCheckRequesterResponse.construct_from_jdict(response.json())
