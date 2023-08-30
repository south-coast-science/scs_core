"""
Created on 17 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://pythoncentral.io/hashing-strings-with-python/

example document:
{"tag": "my-laptop", "attn": "scs-ap1-6", "rec": "2022-11-28T12:05:26Z", "ver": 2.0,
"cmd_tokens": ["test"], "timeout": 20, "digest": "183f9036b2afd0f347ae30f20b228f962ba9731d"}
"""

import hashlib

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable, JSONify

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class ControlDatum(JSONable):
    """
    classdocs
    """

    VERSION = 1.0                   # Version 2.0 is not compatible with deployed devices

    __DEFAULT_TIMEOUT = 30.0        # seconds

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        tag = jdict.get('tag')
        attn = jdict.get('attn')
        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))

        try:
            version = round(float(jdict.get('ver')), 1)
        except (TypeError, ValueError):
            version = None

        cmd_tokens = jdict.get('cmd_tokens')
        timeout = jdict.get('timeout', cls.__DEFAULT_TIMEOUT)
        digest = jdict.get('digest')

        datum = cls(tag, attn, rec, cmd_tokens, timeout, digest, version=version)

        return datum


    @classmethod
    def construct(cls, tag, attn, rec, cmd_tokens, timeout, key):
        digest = cls.__hash(tag, attn, rec, cmd_tokens, key, cls.VERSION)

        return cls(tag, attn, rec, cmd_tokens, timeout, digest, version=cls.VERSION)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __hash(cls, tag, attn, rec, cmd_tokens, key, version):
        rec_iso8601 = rec.as_iso8601(include_millis=Sample.INCLUDE_MILLIS)
        text = str(tag) + str(attn) + JSONify.dumps(rec_iso8601) + str(cmd_tokens) + str(key)

        if version == 2.0:
            hash_object = hashlib.sha1(text.encode())
        else:
            hash_object = hashlib.sha256(text.encode())

        return hash_object.hexdigest()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, attn, rec, cmd_tokens, timeout, digest, version=None):
        """
        Constructor
        """
        self.__tag = tag                    # string - originator of message
        self.__attn = attn                  # string - intended recipient of message
        self.__rec = rec                    # LocalizedDatetime

        self.__version = version            # float

        self.__cmd_tokens = cmd_tokens      # array of { string | int | float }
        self.__timeout = int(timeout)       # int
        self.__digest = digest              # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, key):
        digest = self.__hash(self.tag, self.attn, self.rec, self.cmd_tokens, key, self.version)

        return digest == self.digest


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['attn'] = self.attn
        jdict['rec'] = self.rec.as_iso8601(include_millis=Sample.INCLUDE_MILLIS)

        jdict['ver'] = round(self.version, 1)

        jdict['cmd_tokens'] = self.cmd_tokens
        jdict['timeout'] = self.timeout
        jdict['digest'] = self.digest

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
    def cmd_tokens(self):
        return self.__cmd_tokens


    @property
    def timeout(self):
        return self.__timeout


    @property
    def digest(self):
        return self.__digest


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlDatum:{tag:%s, attn:%s, rec:%s, version:%s, cmd_tokens:%s, timeout:%s, digest:%s}" % \
               (self.tag, self.attn, self.rec, self.version, self.cmd_tokens, self.timeout, self.digest)
