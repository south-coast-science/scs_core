"""
Created on 9 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"topic": "ricardo/gatwick/loc/1/gases", "device": "scs-bgx-507", "rec": "2019-05-10T09:17:39Z",
"expiry": "2019-05-17T09:17:46Z"}
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
        expiry = LocalizedDatetime.construct_from_iso8601(jdict.get('expiry'))

        return cls(topic, device, rec, expiry)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, device, rec, expiry):
        """
        Constructor
        """
        self.__topic = topic                            # string
        self.__device = device                          # string
        self.__rec = rec                                # LocalizedDatetime
        self.__expiry = expiry                          # LocalizedDatetime or None


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
    def next_request(self):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['topic'] = self.topic
        jdict['device'] = self.device
        jdict['rec'] = self.rec
        jdict['expiry'] = self.expiry

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
    def expiry(self):
        return self.__expiry


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{topic:%s, device:%s, rec:%s, expiry:%s}" % \
               (self.topic, self.device, self.rec, self.expiry)
