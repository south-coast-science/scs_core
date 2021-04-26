"""
Created on 24 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"upload": "2018-12-24T13:09:03Z", "rec": "2018-12-24T13:09:01Z", "offset": 2}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class UploadInterval(JSONable):
    """
    classdocs
    """

    UPLOAD_FIELD =      'upload'
    REC_FIELD =         'payload.rec'

    INCLUDE_MILLIS =    False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jstr(cls, jstr):
        if not jstr:
            return None

        # document...
        document = PathDict.construct_from_jstr(jstr)

        if not document:
            return None

        # upload...
        upload_node = document.node(cls.UPLOAD_FIELD)
        upload = LocalizedDatetime.construct_from_iso8601(upload_node)

        if upload is None:
            raise ValueError(upload_node)

        # rec...
        rec_node = document.node(cls.REC_FIELD)
        rec = LocalizedDatetime.construct_from_iso8601(rec_node)

        if rec is None:
            raise ValueError(rec_node)

        # offset...
        offset = upload - rec

        return UploadInterval(upload, rec, offset)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, upload, rec, offset):
        """
        Constructor
        """
        self.__upload = upload              # LocalizedDatetime
        self.__rec = rec                    # LocalizedDatetime

        self.__offset = offset              # Timedelta


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['upload'] = self.upload.as_iso8601(include_millis=self.INCLUDE_MILLIS)
        jdict['rec'] = self.rec.as_iso8601(include_millis=self.INCLUDE_MILLIS)

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
        return "UploadInterval:{upload:%s, rec:%s, offset:%s}" % (self.upload, self.rec, self.offset)
