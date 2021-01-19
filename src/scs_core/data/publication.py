"""
Created on 22 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Publication(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        for topic, payload in jdict.items():
            return Publication(topic, payload)

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, payload):
        """
        Constructor
        """
        self.__topic = topic                    # string
        self.__payload = payload                # dict


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return {self.topic: self.payload}


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def payload(self):
        return self.__payload


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Publication:{topic:%s, payload:%s}" % (self.topic, self.payload)


# --------------------------------------------------------------------------------------------------------------------

class ReceivedPublication(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        received = LocalizedDatetime.construct_from_iso8601(jdict.get('received'))
        message = jdict.get('message')

        return cls(received, message)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, received, message):
        """
        Constructor
        """
        self.__received = received              # LocalizedDatetime
        self.__message = message                # Publication or dict


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['received'] = self.received
        jdict['message'] = self.message

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def received(self):
        return self.__received


    @property
    def message(self):
        return self.__message


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ReceivedPublication:{received:%s, message:%s}" % (self.received, self.message)
