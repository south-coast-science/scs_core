"""
Created on 25 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"device": "scs-be2-3", "topic": "south-coast-science-dev/development/loc/1/gases", "rec": "2018-12-25T20:31:04Z"}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Byline(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device = jdict.get('device')
        topic = jdict.get('topic')

        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('last_write'))         # as provided by web API

        return cls(device, topic, rec)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, topic, rec):
        """
        Constructor
        """
        self.__device = device                      # string tag
        self.__topic = topic                        # string path

        self.__rec = rec                            # LocalizedDatetime


    def __lt__(self, other):
        # device...
        if self.__device < other.__device:
            return True

        if self.__device > other.__device:
            return False

        # topic...
        if self.__topic < other.__topic:
            return True

        if self.__topic > other.__topic:
            return False

        # rec...
        if self.__rec < other.__rec:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['device'] = self.device
        jdict['topic'] = self.topic

        jdict['rec'] = self.rec.as_iso8601()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        return self.__device


    @property
    def topic(self):
        return self.__topic


    @property
    def rec(self):
        return self.__rec


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Byline:{device:%s, topic:%s, rec:%s}" %  (self.device, self.topic, self.rec)
