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

from scs_core.aws.security.cognito_device import CognitoDeviceCredentials

from scs_core.data.array_dict import ArrayDict
from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.topic_path import TopicPath

from scs_core.sys.logging import Logging


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

    def as_json(self, include_message=True):
        jdict = OrderedDict()

        jdict['device'] = self.device
        jdict['topic'] = self.topic

        jdict['lastSeenTime'] = None if self.pub is None else self.pub.as_iso8601()
        jdict['last_write'] = None if self.rec is None else self.rec.as_iso8601()

        if include_message:
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
    def construct_from_jdict(cls, jdict, excluded=None, strict_tags=False, skeleton=False):
        if not jdict:
            return cls({}) if skeleton else None

        bylines = [Byline.construct_from_jdict(byline_jdict) for byline_jdict in jdict]

        return cls.construct(bylines, excluded=excluded, strict_tags=strict_tags)


    @classmethod
    def construct(cls, bylines, excluded=None, strict_tags=False):
        filtered_bylines = []

        for byline in bylines:
            if excluded is not None and byline.topic.endswith(excluded):
                continue

            if strict_tags and not CognitoDeviceCredentials.is_valid_tag(byline.device):
                continue

            filtered_bylines.append(byline)

        # device_bylines...
        device_bylines = ArrayDict([(byline.device, byline) for byline in sorted(filtered_bylines)])

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

    def latest_byline(self, suffix=''):
        latest_byline = None

        for byline in self.bylines:
            if byline.topic.endswith(suffix) and (latest_byline is None or byline.rec > latest_byline.rec):
                latest_byline = byline

        return latest_byline


    def latest_topic(self, suffix=''):
        latest_rec = None
        topic = None

        for byline in self.bylines:
            if byline.topic.endswith(suffix) and (latest_rec is None or byline.rec > latest_rec):
                latest_rec = byline.rec
                topic = byline.topic

        return topic


    def latest_pub(self):
        if not self.bylines:
            return None

        return max([byline.pub for byline in self.bylines if byline.pub is not None], default=None)


    def latest_rec(self):
        if not self.bylines:
            return None

        return max([byline.rec for byline in self.bylines if byline.rec is not None], default=None)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return tuple(byline.as_json() for byline in self.bylines)       # matches the structure of the API response


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def bylines(self):
        for bylines in self._device_bylines.values():
            for byline in bylines:
                yield byline


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{device_bylines:%s}" % self._device_bylines


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
            return device                                       # return the first device tag

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

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def device_byline_group(self, device):
        return DeviceBylineGroup({device: self._device_bylines[device]})


    def bylines_for_device(self, device):
        return self._device_bylines[device]


    def topic_roots(self):
        topic_roots = set()
        for device_tag, bylines in self._device_bylines.items():
            for byline in bylines:
                try:
                    topic_roots.add(TopicPath.construct(byline.rec, byline.topic).root())

                except ValueError:
                    self.__logger.debug("invalid topic: %s" % byline.topic)
                    continue

        return sorted(topic_roots)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def devices(self):
        return list(self._device_bylines.keys())
        # return self._device_bylines.keys()
