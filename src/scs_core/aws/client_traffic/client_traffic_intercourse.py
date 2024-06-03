"""
Created on 8 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

separated from client to remove dependency on requests package
"""
import json
from collections import OrderedDict
from urllib.parse import parse_qs, urlparse

from scs_core.aws.client.api_intercourse import APIResponse
from scs_core.aws.client_traffic.client_traffic import ClientTrafficLocus, ClientTrafficReport

from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class ClientTrafficRequest(ClientTrafficLocus):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        endpoint = qsp.get('endpoint')
        clients = json.loads(qsp.get('clients'))
        period = qsp.get('period')

        aggregate = json.loads(qsp.get('aggregate'))

        return cls(endpoint, clients, period, aggregate)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        endpoint = jdict.get('endpoint')
        clients = jdict.get('clients')
        period = jdict.get('period')

        aggregate = jdict.get('aggregate')

        return cls(endpoint, clients, period, aggregate)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, endpoint, clients, period, aggregate):
        """
        Constructor
        """
        super().__init__(endpoint, clients, period)

        self.__aggregate = bool(aggregate)                          # bool


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            'endpoint': self.endpoint,
            'clients': json.dumps(self.client),
            'period': self.period,
            'aggregate': json.dumps(self.aggregate)
        }

        return params


    def as_json(self, **kwargs):
        jdict = OrderedDict()

        if self.endpoint is not None:
            jdict['endpoint'] = self.endpoint

        jdict['clients'] = self.client
        jdict['period'] = self.period

        jdict['aggregate'] = self.aggregate

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def aggregate(self):
        return self.__aggregate


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientTrafficRequest:{endpoint:%s, clients:%s, period:%s, aggregate:%s}" % \
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

        next_request = jdict.get('next')

        return cls(items, next_request=next_request)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items, next_request=None):
        """
        Constructor
        """
        self.__items = items                                # list of ClientTrafficReport
        self.__next_request = next_request                  # dict (lambda-to-lambda) or URL string (API gateway)


    def __len__(self):
        return len(self.items)


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, _):
        return parse_qs(urlparse(self.next_request).query)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        if self.items is not None:
            jdict['Items'] = self.items
            jdict['itemCount'] = len(self.items)

        if self.next_request is not None:
            jdict['next'] = self.next_request

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return self.__items


    @property
    def next_request(self):
        return self.__next_request


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientTrafficResponse:{items:%s, next_request:%s}" %  (Str.collection(self.items), self.next_request)
