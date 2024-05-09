"""
Created on 8 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.client_traffic.client_traffic_intercourse import ClientTrafficRequest, ClientTrafficResponse
from scs_core.aws.config.endpoint import APIEndpoint


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(APIEndpoint):
    @classmethod
    def configuration(cls):
        return cls('CliTrfAPI/ClientTraffic',
                   'https://tduyom430a.execute-api.us-west-2.amazonaws.com/default/ClientTraffic')


# --------------------------------------------------------------------------------------------------------------------

class ClientTrafficFinder(APIClient):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_users(self, token, request: ClientTrafficRequest):
        url = Endpoint.url('users')

        for item in self._get_blocks(url, token, ClientTrafficResponse, params=request.params()):
            yield item


    def find_for_organisations(self, token, request: ClientTrafficRequest):
        url = Endpoint.url('organisations')

        for item in self._get_blocks(url, token, ClientTrafficResponse, params=request.params()):
            yield item


    def find_for_organisations_users(self, token, request: ClientTrafficRequest):
        url = Endpoint.url('organisations-users')

        for item in self._get_blocks(url, token, ClientTrafficResponse, params=request.params()):
            yield item


    def find_for_endpoint(self, token, request: ClientTrafficRequest):
        url = Endpoint.url('endpoint')

        for item in self._get_blocks(url, token, ClientTrafficResponse, params=request.params()):
            yield item
