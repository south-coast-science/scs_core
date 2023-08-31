"""
Created on 7 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/403421/how-do-i-sort-a-list-of-objects-based-on-an-attribute-of-the-objects

example document:
{"endpoint": "test1", "client": "MyOrg", "period": "2023-08-22", "queries": 99, "invocations": 99, "documents": 495}
"""

import re

from abc import ABC
from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ClientTrafficLocus(ABC, JSONable):
    """
    classdocs
    """

    @classmethod
    def is_valid_period(cls, period):
        try:
            match = re.match(r'^2\d{3}(-[01]\d(-[0123]\d)?)?$', period)
            return match is not None

        except TypeError:
            return False


    @classmethod
    def now(cls):
        return str(LocalizedDatetime.now().utc().datetime.date())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, endpoint, client, period):
        """
        Constructor
        """
        self.__endpoint = endpoint                              # string or None
        self.__client = client                                  # string (or array of) email or int OrgID
        self.__period = period                                  # string (part-)date, e.g. 2023, 2023-08, 2023-08-31


    def __eq__(self, other):
        try:
            return self.endpoint == other.endpoint and self.client == other.client \
                and self.period == other.period

        except (TypeError, AttributeError):
            return False


    def __lt__(self, other):
        if self.endpoint < other.endpoint:
            return True

        if self.endpoint > other.endpoint:
            return False

        if self.client < other.client:
            return True

        if self.client > other.client:
            return False

        if self.period < other.period:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def endpoint(self):
        return self.__endpoint


    @property
    def client(self):
        return self.__client


    @property
    def period(self):
        return self.__period


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientTrafficLocus:{endpoint:%s, client:%s, period:%s}" % \
            (self.endpoint, self.client, self.period)


# --------------------------------------------------------------------------------------------------------------------

class ClientTrafficReport(ClientTrafficLocus):
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

        queries = jdict.get('queries')
        invocations = jdict.get('invocations')
        documents = jdict.get('documents')

        return cls(endpoint, client, period, queries, invocations, documents)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, endpoint, client, period, queries, invocations, documents):
        """
        Constructor
        """
        super().__init__(endpoint, client, period)

        self.__queries = int(queries)                           # int
        self.__invocations = int(invocations)                   # int
        self.__documents = int(documents)                       # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['endpoint'] = self.endpoint
        jdict['client'] = self.client
        jdict['period'] = self.period

        jdict['queries'] = self.queries
        jdict['invocations'] = self.invocations
        jdict['documents'] = self.documents

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def queries(self):
        return self.__queries


    @property
    def invocations(self):
        return self.__invocations


    @property
    def documents(self):
        return self.__documents


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        class_name = self.__class__.__name__

        return class_name + ":{endpoint:%s, client:%s, period:%s, queries:%s, invocations:%s, documents:%s}" % \
            (self.endpoint, self.client, self.period, self.queries, self.invocations, self.documents)
