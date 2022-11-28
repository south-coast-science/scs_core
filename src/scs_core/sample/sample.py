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

    DEFAULT_VERSION = 1.0

    EXEGESIS_TAG =              "exg"
    INCLUDE_MILLIS =            False

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        try:
            version = round(float(jdict.get('ver')), 1)
        except (TypeError, ValueError):
            version = cls.DEFAULT_VERSION

        src = jdict.get('src')
        values = jdict.get('val')
        exegeses = jdict.get('exg')

        return cls(tag, rec, version, src=src, values=values, exegeses=exegeses)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, version, src=None, values=None, exegeses=None):
        """
        Constructor
        """
        self.__tag = tag                                # string
        self.__rec = rec                                # LocalizedDatetime

        self.__version = float(version)                 # float
        self.__src = src                                # string

        self.__values = values                          # OrderedDict
        self.__exegeses = exegeses                      # OrderedDict


    def __eq__(self, other):
        try:
            return self.tag == other.tag and self.rec == other.rec and \
                   self.version == other.version and self.src == other.src and \
                   self.values == other.values and self.exegeses == other.exegeses

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = None if self.rec is None else self.rec.as_iso8601(include_millis=self.INCLUDE_MILLIS)

        if self.tag is not None:
            jdict['tag'] = self.tag

        jdict['ver'] = round(self.version, 1)

        if self.src is not None:
            jdict['src'] = self.src

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


    @rec.setter
    def rec(self, rec):
        self.__rec = rec


    @property
    def version(self):
        return self.__version


    @version.setter
    def version(self, version):
        self.__version = version


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

        return self.__class__.__name__ + ":{tag:%s, rec:%s, version:%s, src:%s, values:%s, exegeses:%s}" % \
            (self.tag, self.rec, self.version, self.src, values, exegeses)
