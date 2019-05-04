"""
Created on 22 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Sample(JSONable):
    """
    classdocs
    """

    INCLUDE_MILLIS = False

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, src, rec, values):
        """
        Constructor
        """
        self.__tag = tag                        # string
        self.__src = src                        # string

        self.__rec = rec                        # LocalizedDatetime

        self.__values = values                  # OrderedDict


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.tag is not None:
            jdict['tag'] = self.tag

        if self.src is not None:
            jdict['src'] = self.src

        jdict['rec'] = self.rec.as_iso8601(self.INCLUDE_MILLIS)
        jdict['val'] = self.values

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def src(self):
        return self.__src


    @property
    def rec(self):
        return self.__rec


    @property
    def values(self):
        return self.__values


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        classname = self.__class__.__name__
        values = '{' + ', '.join(str(key) + ': ' + str(self.values[key]) for key in self.values) + '}'

        return classname + ":{tag:%s, src:%s, rec:%s, values:%s}" % (self.tag, self.src, self.rec, values)
