"""
Created on 22 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"device": "scs-opc-261", "rec": "2024-04-11T11:12:05Z", "upload": "2024-04-22T10:56:50.073Z",
"topic": "southtyneside/cube/loc/261/gases", "expire_at": 1745492210}
"""

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class DuplicatePublication(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device = jdict.get('device')
        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        upload = LocalizedDatetime.construct_from_iso8601(jdict.get('upload'))
        topic = jdict.get('topic')
        expiry = jdict.get('expiry')

        return cls(device, rec, upload, topic, expiry)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, rec, upload, topic, expiry):
        """
        Constructor
        """
        self.__device = device                      # string tag
        self.__rec = rec                            # LocalizedDatetime
        self.__upload = upload                      # LocalizedDatetime
        self.__topic = topic                        # string path
        self.__expiry = expiry                      # LocalizedDatetime


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
            'expiry': self.expiry
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
    def expiry(self):
        return self.__expiry


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DuplicatePublication:{device:%s, rec:%s, upload:%s, topic:%s, expiry:%s}" %  \
               (self.device, self.rec, self.upload, self.topic, self.expiry)
