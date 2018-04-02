"""
Created on 6 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
    "payload":{
        "val":{
            "NO2":{"weV":"0.31288","cnc":"4.0","aeV":"0.310442","weC":"-0.000572"},
            "H2S":{"weV":"0.30813","cnc":"97.7","aeV":"0.282442","weC":"0.090818"},
            "CO":{"weV":"0.596447","cnc":"2076.7","aeV":"0.396444","weC":"0.496341"},
            "pt1":{"v":"0.322474","tmp":"23.0"},
            "sht":{"hmd":"69.6","tmp":"22.3"},
            "SO2":{"weV":"0.279442","cnc":"13.3","aeV":"0.271629","weC":"-0.00096"}
        },
        "rec":"2017-11-03T17:52:45.559+00:00",
        "tag":"scs-be2-2"
    },
    "topic":"south-coast-science-dev/production-test/loc/1/gases",
    "upload":"2017-11-03T17:52:45.559+00:00",
    "device":"scs-bbe-002"
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class MessageCollection(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        items = [Message.construct_from_jdict(msg_jdict) for msg_jdict in jdict.get('Items')]

        count = jdict.get('Count')
        scanned_count = jdict.get('ScannedCount')

        return MessageCollection(items, count, scanned_count)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, items, count, scanned_count):
        """
        Constructor
        """
        self.__items = items                        # list of Message
        self.__count = count                        # int
        self.__scanned_count = scanned_count        # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['Items'] = self.items
        jdict['Count'] = self.count
        jdict['ScannedCount'] = self.scanned_count

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def items(self):
        return self.__items


    @property
    def count(self):
        return self.__count


    @property
    def scanned_count(self):
        return self.__scanned_count


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        items = '[' + ', '.join(str(item) for item in self.items) + ']'

        return "MessageCollection:{items:%s, count:%s, scanned_count:%s}" % \
               (items, self.count, self.scanned_count)


# --------------------------------------------------------------------------------------------------------------------

class Message(JSONable):
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
        upload = LocalizedDatetime.construct_from_iso8601(jdict.get('upload'))

        payload = jdict.get('payload')

        return Message(device, topic, upload, payload)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, topic, upload, payload):
        """
        Constructor
        """
        self.__device = device                  # string
        self.__topic = topic                    # string
        self.__upload = upload                  # LocalizedDatetime

        self.__payload = payload                # string (JSON document)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['device'] = self.device
        jdict['topic'] = self.topic
        jdict['upload'] = self.upload

        jdict['payload'] = self.payload

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        return self.__device


    @property
    def topic(self):
        return self.__topic


    @property
    def upload(self):
        return self.__upload


    @property
    def payload(self):
        return self.__payload


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Message:{device:%s, topic:%s, upload:%s, payload:%s}" % \
               (self.device, self.topic, self.upload, self.payload)
