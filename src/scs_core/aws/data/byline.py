"""
Created on 25 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"device": "scs-bgx-401", "topic": "south-coast-science-demo/brighton/loc/1/climate",
"lastSeenTime": "2020-10-23T08:52:20Z", "last_write": "2020-10-23T08:52:20Z",
"message": "{\"val\": {\"hmd\": 68.4, \"tmp\": 19.8, \"bar\": null}, \"rec\": \"2020-10-23T08:52:20Z\",
\"tag\": \"scs-bgx-401\"}"}
"""

import json

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.str import Str


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

        pub = LocalizedDatetime.construct_from_iso8601(jdict.get('lastSeenTime'))
        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('last_write'))

        try:
            jdict.get('message').keys()
            message = json.dumps(jdict.get('message'))      # web API - message is a dict

        except AttributeError:
            message = jdict.get('message')                  # this class - message is a string

        return cls(device, topic, pub, rec, message)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, topic, pub, rec, message):
        """
        Constructor
        """
        self.__device = device                      # string tag
        self.__topic = topic                        # string path

        self.__pub = pub                            # LocalizedDatetime
        self.__rec = rec                            # LocalizedDatetime

        self.__message = message                    # string


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

        jdict['lastSeenTime'] = None if self.pub is None else self.pub.as_iso8601()
        jdict['last_write'] = None if self.rec is None else self.rec.as_iso8601()

        jdict['message'] = self.message

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


    @property
    def message(self):
        return self.__message


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Byline:{device:%s, topic:%s, pub:%s, rec:%s, message:%s}" %  \
               (self.device, self.topic, self.pub, self.rec, self.message)


# --------------------------------------------------------------------------------------------------------------------

class BylineGroup(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, excluded=None):
        if not jdict:
            return None

        # bylines...
        bylines = []

        for byline_jdict in jdict:
            byline = Byline.construct_from_jdict(byline_jdict)

            if not excluded or not byline.topic.endswith(excluded):
                bylines.append(byline)

        # device_bylines...
        device_bylines = OrderedDict()

        for byline in sorted(bylines):
            if byline.device not in device_bylines:
                device_bylines[byline.device] = []

            device_bylines[byline.device].append(byline)

        return cls(device_bylines)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_bylines):
        """
        Constructor
        """
        self._device_bylines = device_bylines                   # dict of device: Byline


    def __len__(self):
        return len(list(self.bylines))


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
        return [byline.as_json() for byline in self.bylines]    # matches the structure of the API response


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def bylines(self):
        for bylines in self._device_bylines.values():
            for byline in bylines:
                yield byline


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{device_bylines:%s}" % Str.collection(self._device_bylines)


# --------------------------------------------------------------------------------------------------------------------

class DeviceBylineGroup(BylineGroup):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_bylines):
        """
        Constructor
        """
        super().__init__(device_bylines)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        for device in self._device_bylines.keys():
            return device                                       # return the first device

        return None


# --------------------------------------------------------------------------------------------------------------------

class TopicBylineGroup(BylineGroup):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_bylines):
        """
        Constructor
        """
        super().__init__(device_bylines)


    # ----------------------------------------------------------------------------------------------------------------

    def bylines_for_device(self, device):
        return self._device_bylines[device]                     # may raise KeyError


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def devices(self):
        return list(self._device_bylines.keys())
