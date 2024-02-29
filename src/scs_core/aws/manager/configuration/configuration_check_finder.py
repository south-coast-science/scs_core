"""
Created on 28 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.aws import AWS

from scs_core.aws.manager.configuration.configuration_check_intercourse import ConfigurationCheckRequest, \
    ConfigurationCheckResponse


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(object):

    URL = AWS.endpoint_url('ConfChkAPI/ConfigurationCheckFinder',
                           'https://p18hyi3w56.execute-api.us-west-2.amazonaws.com/default/ConfigurationCheckFinder')


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationCheckFinder(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, token, tag_filter, exact_match, response_mode):
        request = ConfigurationCheckRequest(tag_filter, exact_match, response_mode)

        response = requests.get(Endpoint.URL, headers=self._token_headers(token), params=request.params())
        self._check_response(response)

        return ConfigurationCheckResponse.construct_from_jdict(response.json())
