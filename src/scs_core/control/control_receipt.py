"""
Created on 17 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://pythoncentral.io/hashing-strings-with-python/

example document:
{"tag": "scs-ap1-6", "attn": "my-laptop", "rec": "2022-11-28T12:05:27Z", "ver": 2.0,
"cmd": {"cmd": "CMD", "params": [], "stdout": null, "stderr": null, "ret": 0},
"omd": "183f9036b2afd0f347ae30f20b228f962ba9731d", "digest": "9360daca435f4a50c35123452003e56cb756d0a9"}
"""

import hashlib

from collections import OrderedDict

from scs_core.control.command import Command

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable, JSONify

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class ControlReceipt(JSONable):
    """
    classdocs
    """

    VERSION = 2.0

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        tag = jdict.get('tag')
        attn = jdict.get('attn')

        try:
            version = round(float(jdict.get('ver')), 1)
        except (TypeError, ValueError):
            version = None

        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        command = Command.construct_from_jdict(jdict.get('cmd'))
        omd = jdict.get('omd')
        digest = jdict.get('digest')

        datum = cls(tag, attn, rec, command, omd, digest, version=version)

        return datum


    @classmethod
    def construct_from_datum(cls, datum, rec, command, key):
        digest = ControlReceipt.__hash(datum.attn, rec, command, datum.digest, key, cls.VERSION)

        return cls(datum.attn, datum.tag, rec, command, datum.digest, digest, version=cls.VERSION)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __hash(cls, tag, rec, command, omd, key, version):
        rec_iso8601 = rec.as_iso8601(include_millis=Sample.INCLUDE_MILLIS)
        text = str(tag) + JSONify.dumps(rec_iso8601) + JSONify.dumps(command) + str(omd) + str(key)

        if version == 2.0:
            hash_object = hashlib.sha1(text.encode())
        else:
            hash_object = hashlib.sha256(text.encode())

        return hash_object.hexdigest()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, attn, rec, command, omd, digest, version=None):
        """
        Constructor
        """
        self.__tag = tag                    # string
        self.__attn = attn                  # string
        self.__rec = rec                    # LocalizedDatetime

        self.__version = version            # float

        self.__command = command            # Command
        self.__omd = omd                    # string
        self.__digest = digest              # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, key):
        digest = self.__hash(self.tag, self.rec, self.command, self.omd, key, self.version)

        return digest == self.__digest


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['attn'] = self.attn
        jdict['rec'] = self.rec.as_iso8601(include_millis=Sample.INCLUDE_MILLIS)

        jdict['ver'] = round(self.version, 1)

        jdict['cmd'] = self.command
        jdict['omd'] = self.omd
        jdict['digest'] = self.__digest

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def attn(self):
        return self.__attn


    @property
    def rec(self):
        return self.__rec


    @property
    def version(self):
        return self.__version


    @property
    def command(self):
        return self.__command


    @property
    def omd(self):
        return self.__omd


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlReceipt:{tag:%s, attn:%s, rec:%s, version:%s, command:%s, omd:%s, digest:%s}" % \
               (self.tag, self.attn, self.rec, self.version, self.command, self.omd, self.__digest)
