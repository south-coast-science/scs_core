"""
Created on 8 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.client_traffic.client_traffic_intercourse import ClientTrafficResponse


# --------------------------------------------------------------------------------------------------------------------

class ClientTrafficFinder(APIClient):
    """
    classdocs
    """

    __URL = 'https://tduyom430a.execute-api.us-west-2.amazonaws.com/default/ClientTraffic'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_users(self, token, request):
        url = '/'.join((self.__URL, 'users'))

        for item in self._get_blocks(url, token, ClientTrafficResponse, payload=request):
            yield item


    def find_for_organisations(self, token, request):
        url = '/'.join((self.__URL, 'organisations'))

        for item in self._get_blocks(url, token, ClientTrafficResponse, payload=request):
            yield item


    def find_for_organisations_users(self, token, request):
        url = '/'.join((self.__URL, 'organisations-users'))

        for item in self._get_blocks(url, token, ClientTrafficResponse, payload=request):
            yield item
