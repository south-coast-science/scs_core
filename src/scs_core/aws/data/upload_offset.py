"""
Created on 24 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class UploadOffset(JSONable):
    """
    classdocs
    """

    INCLUDE_MILLIS = False

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        upload = LocalizedDatetime.construct_from_iso8601(jdict.get('upload'))
        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('val.rec'))

        offset = jdict.get('offset')

        return UploadOffset(upload, rec, offset)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, upload, rec, offset):
        """
        Constructor
        """
        self.__upload = upload              # LocalizedDatetime
        self.__rec = rec                    # LocalizedDatetime

        self.__offset = offset              # timedelta


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['upload'] = self.upload.as_iso8601(self.INCLUDE_MILLIS)
        jdict['rec'] = self.upload.as_iso8601(self.INCLUDE_MILLIS)

        jdict['offset'] = self.offset

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def upload(self):
        return self.__upload


    @property
    def rec(self):
        return self.__rec


    @property
    def offset(self):
        return self.__offset


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UploadOffset:{upload:%s, rec:%s, offset:%s}" % \
               (self.upload, self.rec, self.offset)
