"""
Created on 9 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.manager.topic_origin.topic_origin_intercourse import TopicOriginRequest, TopicOriginResponse


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('OriginAPI/TopicOrigin',
                   'https://7qos9nwc7k.execute-api.us-west-2.amazonaws.com/default/TopicOrigin')


# --------------------------------------------------------------------------------------------------------------------

class TopicOriginFinder(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find(self, token, topic):
        request = TopicOriginRequest(topic)

        response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=request.params())
        self._check_response(response)

        return TopicOriginResponse.construct_from_jdict(response.json())
