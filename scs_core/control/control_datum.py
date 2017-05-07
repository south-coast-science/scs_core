"""
Created on 17 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://pythoncentral.io/hashing-strings-with-python/
"""

import hashlib

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.localized_datetime import LocalizedDatetime


# TODO: add requester tag

# --------------------------------------------------------------------------------------------------------------------

class ControlDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        cmd = jdict.get('cmd')
        params = jdict.get('params')
        digest = jdict.get('digest')

        datum = ControlDatum(tag, rec, cmd, params, digest)

        return datum


    @classmethod
    def construct(cls, tag, rec, cmd, params, subscriber_sn):
        digest = ControlDatum.__hash(tag, rec, cmd, params, subscriber_sn)

        return ControlDatum(tag, rec, cmd, params, digest)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __hash(cls, tag, rec, cmd, params, subscriber_sn):
        text = str(tag) + rec.as_json() + str(cmd) + str(params) + str(subscriber_sn)
        hash_object = hashlib.sha256(text.encode())

        return hash_object.hexdigest()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, cmd, params, digest):
        """
        Constructor
        """
        self.__tag = tag                # string
        self.__rec = rec                # LocalizedDatetime
        self.__cmd = cmd                # string
        self.__params = params          # array of { string | int | float }
        self.__digest = digest          # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, subscriber_sn):
        digest = ControlDatum.__hash(self.tag, self.rec, self.cmd, self.params, subscriber_sn)

        return digest == self.digest


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['rec'] = self.rec
        jdict['cmd'] = self.cmd
        jdict['params'] = self.params
        jdict['digest'] = self.digest

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def rec(self):
        return self.__rec


    @property
    def cmd(self):
        return self.__cmd


    @property
    def params(self):
        return self.__params


    @property
    def digest(self):
        return self.__digest


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlDatum:{tag:%s, rec:%s, cmd:%s, params:%s, digest:%s}" % \
               (self.tag, self.rec, self.cmd, self.params, self.digest)
