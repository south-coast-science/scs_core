"""
Created on 9 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.manager.topic_origin.topic_origin import TopicOrigin


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

    BLOCK_SIZE = 100                    # maximum number of topics per request

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reporter=None):
        super().__init__(reporter=reporter)


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_topics(self, token, topics):
        if self._reporter:
            self._reporter.reset()

        origins = []

        for index in range(0, len(topics), self.BLOCK_SIZE):
            request = topics[index:index + self.BLOCK_SIZE]
            params = {"topics": json.dumps(request)}

            response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=params)
            self._check_response(response)

            block = [TopicOrigin.construct_from_jdict(jdict) for jdict in response.json()]
            origins.extend(block)

            if self._reporter:
                self._reporter.print(len(block))

        return sorted(origins)
