"""
Created on 17 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://pythoncentral.io/hashing-strings-with-python/
"""

import hashlib

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.localized_datetime import LocalizedDatetime


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
        date = LocalizedDatetime.construct_from_iso8601(jdict.get('date'))
        cmd = jdict.get('cmd')
        params = jdict.get('params')
        digest = jdict.get('digest')

        datum = ControlDatum(tag, date, cmd, params, digest)

        return datum


    @classmethod
    def construct(cls, tag, date, cmd, params, subscriber_sn):
        digest = ControlDatum.__hash(tag, date, cmd, params, subscriber_sn)

        return ControlDatum(tag, date, cmd, params, digest)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __hash(cls, tag, date, cmd, params, subscriber_sn):
        text = str(tag) + date.as_json() + str(cmd) + str(params) + str(subscriber_sn)
        hash_object = hashlib.sha256(text.encode())

        return hash_object.hexdigest()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, date, cmd, params, digest):
        """
        Constructor
        """
        self.__tag = tag                # string
        self.__date = date              # LocalizedDatetime
        self.__cmd = cmd                # string
        self.__params = params          # array of { string | int | float }
        self.__digest = digest          # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, subscriber_sn):
        digest = ControlDatum.__hash(self.tag, self.date, self.cmd, self.params, subscriber_sn)

        return digest == self.digest


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['date'] = self.date
        jdict['cmd'] = self.cmd
        jdict['params'] = self.params
        jdict['digest'] = self.digest

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def date(self):
        return self.__date


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
        return "ControlDatum:{tag:%s, date:%s, cmd:%s, params:%s, digest:%s}" % \
               (self.tag, self.date, self.cmd, self.params, self.digest)
