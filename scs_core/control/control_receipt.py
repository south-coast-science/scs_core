"""
Created on 17 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://pythoncentral.io/hashing-strings-with-python/
"""

import hashlib

from collections import OrderedDict

from scs_core.control.command import Command

from scs_core.data.json import JSONable
from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class ControlReceipt(JSONable):
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
        command = Command.construct_from_jdict(jdict.get('cmd'))
        omd = jdict.get('omd')
        digest = jdict.get('digest')

        datum = ControlReceipt(tag, rec, command, omd, digest)

        return datum


    @classmethod
    def construct_from_datum(cls, datum, rec, command, subscriber_sn):
        digest = ControlReceipt.__hash(datum.attn, rec, command, datum.digest, subscriber_sn)

        return ControlReceipt(datum.attn, rec, command, datum.digest, digest)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __hash(cls, tag, rec, command, omd, subscriber_sn):
        text = str(tag) + JSONify.dumps(rec) + JSONify.dumps(command) + str(omd) + str(subscriber_sn)
        hash_object = hashlib.sha256(text.encode())

        return hash_object.hexdigest()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, command, omd, digest):
        """
        Constructor
        """
        self.__tag = tag                    # string

        self.__rec = rec                    # LocalizedDatetime
        self.__command = command            # Command
        self.__omd = omd                    # string
        self.__digest = digest              # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, subscriber_sn):
        digest = ControlReceipt.__hash(self.tag, self.rec, self.command, self.omd, subscriber_sn)

        return digest == self.__digest


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag

        jdict['rec'] = self.rec
        jdict['cmd'] = self.command
        jdict['omd'] = self.omd
        jdict['digest'] = self.__digest

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def rec(self):
        return self.__rec


    @property
    def command(self):
        return self.__command


    @property
    def omd(self):
        return self.__omd


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlReceipt:{tag:%s, rec:%s, command:%s, omd:%s, digest:%s}" % \
               (self.tag, self.rec, self.command, self.omd, self.__digest)
