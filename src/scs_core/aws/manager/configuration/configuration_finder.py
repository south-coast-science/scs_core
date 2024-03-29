"""
Created on 07 Apr 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
"""

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.manager.configuration.configuration_intercourse import ConfigurationRequest, ConfigurationResponse


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('ConfAPI/ConfigurationFinder',
                   'https://p18hyi3w56.execute-api.us-west-2.amazonaws.com/default/ConfigurationFinder')


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationFinder(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reporter=None):
        super().__init__(reporter=reporter)


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, token, tag_filter, exact_match, response_mode):
        if self._reporter:
            self._reporter.reset()

        request = ConfigurationRequest(tag_filter, exact_match, response_mode)

        for item in self._get_blocks(Endpoint.url(), token, ConfigurationResponse, params=request.params()):
            yield item
