"""
Created on 22 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class Sample(JSONable):
    """
    classdocs
    """

    EXEGESIS_TAG =              "exg"
    INCLUDE_MILLIS =            False

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        tag = jdict.get('tag')
        src = jdict.get('src')
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))
        values = jdict.get('val')
        exegeses = jdict.get('exg')

        return cls(tag, rec, src=src, values=values, exegeses=exegeses)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, src=None, values=None, exegeses=None):
        """
        Constructor
        """
        self.__tag = tag                        # string
        self.__rec = rec                        # LocalizedDatetime

        self.__src = src                        # string
        self.__values = values                  # OrderedDict
        self.__exegeses = exegeses              # OrderedDict


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.tag is not None:
            jdict['tag'] = self.tag

        if self.src is not None:
            jdict['src'] = self.src

        jdict['rec'] = None if self.rec is None else self.rec.as_iso8601(self.INCLUDE_MILLIS)
        jdict['val'] = self.values

        if self.exegeses:
            jdict[self.EXEGESIS_TAG] = self.exegeses

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def rec(self):
        return self.__rec


    @property
    def src(self):
        return self.__src


    @property
    def values(self):
        return self.__values


    @property
    def exegeses(self):
        return self.__exegeses


    @exegeses.setter
    def exegeses(self, exegeses):
        self.__exegeses = exegeses


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        values = Str.collection(self.values)
        exegeses = Str.collection(self.exegeses)

        return self.__class__.__name__ + ":{tag:%s, rec:%s, src:%s, values:%s, exegeses:%s}" % \
            (self.tag, self.rec, self.src, values, exegeses)
