"""
Created on 22 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.data.ingestion.duplicate_publication import DuplicatePublication


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('TopMonAPI/DuplicatePublication',
                   'https://nfema83f18.execute-api.us-west-2.amazonaws.com/default/DuplicatePublication')


# --------------------------------------------------------------------------------------------------------------------

class DuplicatePublicationFinder(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, reporter=None):
        super().__init__(reporter=reporter)


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self, token):
        return self.__find(token)


    def find_for_device(self, token, device):
        return self.__find(token, params={'device': device})


    # ----------------------------------------------------------------------------------------------------------------

    def __find(self, token, params=None):
        if self._reporter:
            self._reporter.reset()

        duplicates = []

        response = requests.get(Endpoint.url(), headers=self._token_headers(token), params=params)
        self._check_response(response)

        block = [DuplicatePublication.construct_from_jdict(jdict) for jdict in response.json()]
        duplicates.extend(block)

        if self._reporter:
            self._reporter.print(len(block))

        return sorted(duplicates)
