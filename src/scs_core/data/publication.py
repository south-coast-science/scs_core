"""
Created on 22 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

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
        self.__payload = payload                # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict[self.topic] = self.payload

        return jdict


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
