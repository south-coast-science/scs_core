"""
Created on 25 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"device": "scs-bgx-401", "topic": "south-coast-science-demo/brighton/loc/1/particulates",
"latest-pub": "2020-09-25T11:49:46Z", "latest-rec": "2020-09-25T11:49:40Z"}
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

        latest_pub = LocalizedDatetime.construct_from_iso8601(jdict.get('lastSeenTime'))    # as provided by web API
        latest_rec = LocalizedDatetime.construct_from_iso8601(jdict.get('last_write'))      # as provided by web API

        return cls(device, topic, latest_pub, latest_rec)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, topic, latest_pub, latest_rec):
        """
        Constructor
        """
        self.__device = device                      # string tag
        self.__topic = topic                        # string path

        self.__latest_pub = latest_pub              # LocalizedDatetime
        self.__latest_rec = latest_rec              # LocalizedDatetime


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

        # latest_rec...
        if self.__latest_rec < other.__latest_rec:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['device'] = self.device
        jdict['topic'] = self.topic

        jdict['latest-pub'] = self.__latest_pub.as_iso8601()
        jdict['latest-rec'] = self.latest_rec.as_iso8601()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        return self.__device


    @property
    def topic(self):
        return self.__topic


    @property
    def latest_pub(self):
        return self.__latest_pub


    @property
    def latest_rec(self):
        return self.__latest_rec


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Byline:{device:%s, topic:%s, latest_pub:%s, latest_rec:%s}" %  \
               (self.device, self.topic, self.latest_pub, self.latest_rec)
