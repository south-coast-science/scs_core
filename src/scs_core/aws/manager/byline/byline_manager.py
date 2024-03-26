"""
Created on 26 Mar 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('BylineAPI/TopicBylines',
                   'https://k5uz49605m.execute-api.us-west-2.amazonaws.com/default/TopicBylines')


# --------------------------------------------------------------------------------------------------------------------

class BylineManager(APIClient):
    """
    classdocs
    """

    DEVICE = 'device'
    TOPIC = 'topic'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def delete(self, token, device_tag, topic):
        params = {'device': device_tag, 'topic': topic}

        response = requests.delete(Endpoint.url(), headers=self._token_headers(token), params=params)
        self._check_response(response)
