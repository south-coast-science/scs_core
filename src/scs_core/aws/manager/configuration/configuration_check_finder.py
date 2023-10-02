"""
Created on 28 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.manager.configuration.configuration_check_intercourse import ConfigurationCheckRequest, \
    ConfigurationCheckResponse


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheckFinder(APIClient):
    """
    classdocs
    """

    __URL = "https://p18hyi3w56.execute-api.us-west-2.amazonaws.com/default/ConfigurationCheckFinder"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, token, tag_filter, exact_match, response_mode):
        request = ConfigurationCheckRequest(tag_filter, exact_match, response_mode)

        response = requests.get(self.__URL, headers=self._token_headers(token), params=request.params())
        self._check_response(response)

        return ConfigurationCheckResponse.construct_from_jdict(response.json())
