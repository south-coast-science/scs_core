"""
Created on 22 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import requests

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.config.endpoint import APIEndpoint
from scs_core.aws.data.ingestion.duplicate_publication import DuplicatePublication, DuplicatePublicationSummary


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

    def find_summaries(self, token):
        url = '/'.join([Endpoint.url(), 'summaries'])

        response = requests.get(url, headers=self._token_headers(token))
        self._check_response(response)

        return sorted([DuplicatePublicationSummary.construct_from_jdict(jdict) for jdict in response.json()])


    def find_for_device(self, token, device):
        url = '/'.join([Endpoint.url(), 'device'])
        params = {'device': device}

        response = requests.get(url, headers=self._token_headers(token), params=params)
        self._check_response(response)

        return sorted([DuplicatePublication.construct_from_jdict(jdict) for jdict in response.json()])
