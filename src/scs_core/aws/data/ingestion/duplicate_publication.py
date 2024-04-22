"""
Created on 22 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"device": "scs-opc-261", "rec": "2024-04-11T11:12:05Z", "upload": "2024-04-22T10:56:50.073Z",
"topic": "southtyneside/cube/loc/261/gases", "expire_at": 1745492210}
"""

from scs_core.aws.data.ingestion.ingestible_message import IngestibleMessage

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class DuplicatePublication(JSONable):
    """
    classdocs
    """

    TTL = Timedelta(days=367)

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device = jdict.get('device')
        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        upload = LocalizedDatetime.construct_from_iso8601(jdict.get('upload'))
        topic = jdict.get('topic')
        expire_at = jdict.get('expire_at')

        return cls(device, rec, upload, topic, expire_at)


    @classmethod
    def construct_from_message(cls, message: IngestibleMessage):
        device = message.device
        rec = message.rec_at
        upload = message.upload
        topic = message.topic

        expire_at = upload + cls.TTL

        return cls(device, rec, upload, topic, expire_at)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, rec, upload, topic, expire_at):
        """
        Constructor
        """
        self.__device = device                      # string tag
        self.__rec = rec                            # LocalizedDatetime
        self.__upload = upload                      # LocalizedDatetime
        self.__topic = topic                        # string path
        self.__expire_at = expire_at                # LocalizedDatetime


    def __lt__(self, other):
        # device...
        if self.__device < other.__device:
            return True

        if self.__device > other.__device:
            return False

        # rec...
        if self.__rec < other.__rec:
            return True

        if self.__rec > other.__drec:
            return False

        # upload...
        if self.__upload < other.__upload:
            return True

        if self.__upload > other.__upload:
            return False

        # topic...
        return self.__topic < other.__topic


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = {
            'device': self.device,
            'rec': self.rec.as_iso8601(),
            'upload': self.upload.as_iso8601(include_millis=True),
            'topic': self.topic,
            'expire_at': int(self.expire_at.timestamp())
        }

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        return self.__device


    @property
    def rec(self):
        return self.__rec


    @property
    def upload(self):
        return self.__upload


    @property
    def topic(self):
        return self.__topic


    @property
    def expire_at(self):
        return self.__expire_at


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DuplicatePublication:{device:%s, rec:%s, upload:%s, topic:%s, expire_at:%s}" %  \
               (self.device, self.rec, self.upload, self.topic, self.expire_at)
