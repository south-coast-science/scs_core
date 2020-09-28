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

        pub = LocalizedDatetime.construct_from_iso8601(jdict.get('lastSeenTime'))    # as provided by web API
        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('last_write'))      # as provided by web API

        return cls(device, topic, pub, rec)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, topic, pub, rec):
        """
        Constructor
        """
        self.__device = device                      # string tag
        self.__topic = topic                        # string path

        self.__pub = pub                            # LocalizedDatetime
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
        if self.__rec is None:
            return True

        if other.__rec is None:
            return False

        if self.__rec < other.__rec:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['device'] = self.device
        jdict['topic'] = self.topic

        jdict['latest-pub'] = None if self.pub is None else self.pub.as_iso8601()
        jdict['latest-rec'] = None if self.rec is None else self.rec.as_iso8601()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        return self.__device


    @property
    def topic(self):
        return self.__topic


    @property
    def pub(self):
        return self.__pub


    @property
    def rec(self):
        return self.__rec


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Byline:{device:%s, topic:%s, pub:%s, rec:%s}" %  \
               (self.device, self.topic, self.pub, self.rec)


# --------------------------------------------------------------------------------------------------------------------

class BylineGroup(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        return cls(sorted([Byline.construct_from_jdict(byline_jdict) for byline_jdict in jdict]))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, bylines):
        """
        Constructor
        """
        self.__bylines = bylines                    # list of Byline


    def __len__(self):
        return len(self.bylines)


    # ----------------------------------------------------------------------------------------------------------------

    def latest_pub(self):
        if not self.bylines:
            return None

        return max([byline.pub for byline in self.bylines if byline.pub is not None])


    def latest_rec(self):
        if not self.bylines:
            return None

        return max([byline.rec for byline in self.bylines if byline.rec is not None])


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['bylines'] = self.bylines

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def bylines(self):
        return self.__bylines


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BylineGroup:{bylines:%s}" %  self.bylines
