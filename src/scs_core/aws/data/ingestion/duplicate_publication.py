"""
Created on 22 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example DuplicatePublication:
{"device": "scs-opc-261", "rec": "2024-04-11T11:12:05Z", "upload": "2024-04-22T14:10:04.982Z",
"expiry": "2024-04-12T11:12:05Z"}

example DuplicatePublicationSummary:
{"device": "scs-opc-268", "count": 2}
"""

from collections import OrderedDict

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
        expiry = LocalizedDatetime.construct_from_iso8601(jdict.get('expiry'))

        return cls(device, rec, upload, expiry=expiry)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, rec, upload, expiry=None):
        """
        Constructor
        """
        self.__device = device                      # string tag
        self.__rec = rec                            # LocalizedDatetime
        self.__upload = upload                      # LocalizedDatetime
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

        if self.__rec > other.__rec:
            return False

        # upload...
        return self.__upload < other.__upload


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, include_expiry=True, **kwargs):
        jdict = OrderedDict()

        jdict['device'] = self.device
        jdict['rec'] = self.rec.as_iso8601()
        jdict['upload'] = self.upload.as_iso8601(include_millis=True)

        if include_expiry:
            jdict['expiry'] = self.expiry

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
    def expiry(self):
        return self.__expiry


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{device:%s, rec:%s, upload:%s, expiry:%s}" % \
               (self.device, self.rec, self.upload, self.expiry)


# --------------------------------------------------------------------------------------------------------------------

class DuplicatePublicationSummary(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device = jdict.get('device')
        count = jdict.get('count')

        return cls(device, count)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, count):
        """
        Constructor
        """
        self.__device = device                      # string tag
        self.__count = int(count)                   # int


    # ----------------------------------------------------------------------------------------------------------------

    def inc(self):
        self.__count += 1


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = {
            'device': self.device,
            'count': self.count
        }

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        return self.__device


    @property
    def count(self):
        return self.__count


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{device:%s, count:%s}" % (self.device, self.count)


# --------------------------------------------------------------------------------------------------------------------

class DeviceSummary(DuplicatePublicationSummary):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, count):
        """
        Constructor
        """
        super().__init__(device, count)


    def __lt__(self, other):
        # count...
        if self.device < other.device:
            return True

        if self.device > other.device:
            return False

        # device...
        return self.count < other.count


# --------------------------------------------------------------------------------------------------------------------

class CountSummary(DuplicatePublicationSummary):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, count):
        """
        Constructor
        """
        super().__init__(device, count)


    def __lt__(self, other):
        # count...
        if self.count < other.count:
            return True

        if self.count > other.count:
            return False

        # device...
        return self.device < other.device
