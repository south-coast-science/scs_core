"""
Created on 9 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"topic": "south-coast-science-dev/development/loc/1/climate", "device": "scs-be2-3", "rec": "2023-03-14T00:00:03Z"}
"""

from collections import OrderedDict

from scs_core.aws.client.api_intercourse import APIResponse
from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class TopicOrigin(APIResponse):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        topic = jdict.get('topic')
        device = jdict.get('device')
        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        exipry = LocalizedDatetime.construct_from_iso8601(jdict.get('exipry'))

        return cls(topic, device, rec, exipry)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, device, rec, exipry):
        """
        Constructor
        """
        self.__topic = topic                            # string
        self.__device = device                          # string
        self.__rec = rec                                # LocalizedDatetime
        self.__exipry = exipry                          # LocalizedDatetime or None


    def __lt__(self, other):
        if self.rec < other.rec:
            return True

        if self.rec > other.rec:
            return False

        if self.topic < other.topic:
            return True

        if self.topic > other.topic:
            return True

        return self.device < other.device


    # ----------------------------------------------------------------------------------------------------------------

    def next_params(self, params):
        raise NotImplementedError


    @property
    def next_url(self):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['topic'] = self.topic
        jdict['device'] = self.device
        jdict['rec'] = self.rec
        jdict['exipry'] = self.exipry

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def device(self):
        return self.__device


    @property
    def rec(self):
        return self.__rec


    @property
    def exipry(self):
        return self.__exipry


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicOrigin:{topic:%s, device:%s, rec:%s, exipry:%s}" % \
               (self.topic, self.device, self.rec, self.exipry)
