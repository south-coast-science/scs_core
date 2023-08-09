"""
Created on 8 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from urllib.parse import parse_qs, urlparse

from scs_core.aws.client.api_client import APIClient, APIResponse
from scs_core.aws.security.client_traffic import ClientTrafficLocus, ClientTrafficReport

from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class ClientTrafficFinder(APIClient):
    """
    classdocs
    """

    __URL = 'https://xxxxxxx.execute-api.us-west-2.amazonaws.com/default/ClientTraffic/'

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        super().__init__()


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_user(self, token, request):
        url = '/'.join((self.__URL, 'user'))

        for item in self._get_blocks(url, token, ClientTrafficResponse, payload=request):
            yield item


    def find_for_organisation(self, token, request):
        url = '/'.join((self.__URL, 'organisation'))

        for item in self._get_blocks(url, token, ClientTrafficResponse, payload=request):
            yield item


# --------------------------------------------------------------------------------------------------------------------

class ClientTrafficRequest(ClientTrafficLocus):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        endpoint = jdict.get('endpoint')
        client = jdict.get('client')
        period = jdict.get('period')

        aggregate = jdict.get('aggregate')

        return cls(endpoint, client, period, aggregate)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, endpoint, client, period, aggregate):
        """
        Constructor
        """
        super().__init__(endpoint, client, period)

        self.__aggregate = bool(aggregate)                          # bool


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['endpoint'] = self.endpoint
        jdict['client'] = self.client
        jdict['period'] = self.period

        jdict['aggregate'] = self.aggregate

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def aggregate(self):
        return self.__aggregate


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientTrafficRequest:{endpoint:%s, client:%s, period:%s, aggregate:%s}" % \
            (self.endpoint, self.client, self.period, self.aggregate)


# --------------------------------------------------------------------------------------------------------------------

class ClientTrafficResponse(APIResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        items = []
        if jdict.get('Items'):
            for item_jdict in jdict.get('Items'):
                item = ClientTrafficReport.construct_from_jdict(item_jdict)
                items.append(item)

        next_url = jdict.get('next')

        return cls(items, next_url=next_url)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items, next_url=None):
        """
        Constructor
        """
        self.__items = items                                # list of ClientTrafficReport
        self.__next_url = next_url                          # URL string


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, _):
        return parse_qs(urlparse(self.next_url).query)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.items is not None:
            jdict['Items'] = self.items
            jdict['itemCount'] = len(self.items)

        if self.next_url is not None:
            jdict['next'] = self.next_url

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return self.__items


    @property
    def next_url(self):
        return self.__next_url


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientTrafficResponse:{items:%s, next_url:%s}" %  (Str.collection(self.items), self.next_url)
