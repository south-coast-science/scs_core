"""
Created on 17 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://pythoncentral.io/hashing-strings-with-python/

example document:
{"tag": "bruno.lan",
"attn": "scs-be2-3",
"rec": "2017-08-29T11:12:31.636+01:00",
"cmd_tokens": ["?"],
"digest": "6e81c77aa20562ea06e0e32158d2c7c9431ed251cd5790917f6cb385f6cf62c0"}
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

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        tag = jdict.get('tag')
        attn = jdict.get('attn')

        rec = LocalizedDatetime.construct_from_iso8601(jdict.get('rec'))
        cmd_tokens = jdict.get('cmd_tokens')
        digest = jdict.get('digest')

        datum = ControlDatum(tag, attn, rec, cmd_tokens, digest)

        return datum


    @classmethod
    def construct(cls, tag, attn, rec, cmd_tokens, key):
        digest = cls.__hash(tag, attn, rec, cmd_tokens, key)

        return ControlDatum(tag, attn, rec, cmd_tokens, digest)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __hash(cls, tag, attn, rec, cmd_tokens, key):
        rec_iso8601 = rec.as_iso8601(Sample.INCLUDE_MILLIS)

        text = str(tag) + str(attn) + JSONify.dumps(rec_iso8601) + str(cmd_tokens) + str(key)
        hash_object = hashlib.sha256(text.encode())

        return hash_object.hexdigest()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, attn, rec, cmd_tokens, digest):
        """
        Constructor
        """
        self.__tag = tag                    # string - originator of message
        self.__attn = attn                  # string - intended recipient of message

        self.__rec = rec                    # LocalizedDatetime
        self.__cmd_tokens = cmd_tokens      # array of { string | int | float }
        self.__digest = digest              # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self, key):
        digest = ControlDatum.__hash(self.tag, self.attn, self.rec, self.cmd_tokens, key)

        return digest == self.digest


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['attn'] = self.attn

        jdict['rec'] = self.rec.as_iso8601(Sample.INCLUDE_MILLIS)

        jdict['cmd_tokens'] = self.cmd_tokens
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
    def cmd_tokens(self):
        return self.__cmd_tokens


    @property
    def digest(self):
        return self.__digest


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ControlDatum:{tag:%s, attn:%s, rec:%s, cmd_tokens:%s, digest:%s}" % \
               (self.tag, self.attn, self.rec, self.cmd_tokens, self.digest)
