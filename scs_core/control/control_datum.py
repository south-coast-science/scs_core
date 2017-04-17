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
        time = LocalizedDatetime.construct_from_iso8601(jdict.get('time'))
        command = jdict.get('command')
        params = jdict.get('params')
        digest = jdict.get('digest')

        datum = ControlDatum(tag, time, command, params, digest)

        return datum


    @classmethod
    def construct(cls, tag, time, command, params, subscriber_sn):
        digest = ControlDatum.__hash(tag, time, command, params, subscriber_sn)

        return ControlDatum(tag, time, command, params, digest)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __hash(cls, tag, time, command, params, subscriber_sn):
        text = str(tag) + time.as_json() + str(command) + str(params) + str(subscriber_sn)
        hash_object = hashlib.sha256(text.encode())

        return hash_object.hexdigest()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, time, command, params, digest):
        """
        Constructor
        """
        self.__tag = tag                # string
        self.__time = time              # LocalizedDatetime
        self.__command = command        # string
        self.__params = params          # array of { string | int | float }
        self.__digest = digest          # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, subscriber_sn):
        digest = ControlDatum.__hash(self.tag, self.time, self.command, self.params, subscriber_sn)

        return digest == self.__digest


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['time'] = self.time
        jdict['command'] = self.command
        jdict['params'] = self.params
        jdict['digest'] = self.__digest

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def time(self):
        return self.__time


    @property
    def command(self):
        return self.__command


    @property
    def params(self):
        return self.__params


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlDatum:{tag:%s, time:%s, command:%s, params:%s, digest:%s}" % \
               (self.tag, self.time, self.command, self.params, self.__digest)
