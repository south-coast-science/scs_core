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

class TopicOriginRequest(object):
    """
    classdocs
    """

    TOPIC = 'topic'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        topic = qsp.get(cls.TOPIC)

        return cls(topic)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic):
        """
        Constructor
        """
        self.__topic = topic                                                        # string


    # ----------------------------------------------------------------------------------------------------------------

    def params(self):
        params = {
            self.TOPIC: self.topic,
        }

        return params


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicOriginRequest:{topic:%s}" % self.topic


# --------------------------------------------------------------------------------------------------------------------

class TopicOriginResponse(APIResponse):
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

        return cls(topic, device, rec)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, device, rec):
        """
        Constructor
        """
        self.__topic = topic                            # string
        self.__device = device                          # string
        self.__rec = rec                                # LocalizedDatetime


    def __lt__(self, other):
        if self.topic < other.topic:
            return True

        if self.topic > other.topic:
            return False

        if self.device < other.device:
            return True

        if self.device > other.device:
            return True

        return self.rec < other.rec


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


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicOriginResponse:{topic:%s, device:%s, rec:%s}" % \
               (self.topic, self.device, self.rec)
