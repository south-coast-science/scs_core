"""
Created on 22 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SampleDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, *values):
        """
        Constructor
        """
        self.__rec = rec                        # LocalizedDatetime
        self.__val = OrderedDict(values)        # OrderedDict of (src, JSONable)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec
        jdict['val'] = self.val

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def val(self):
        return self.__val


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        vals = '[' + ', '.join([str(key) + ': ' + str(self.val[key]) for key in self.val]) + ']'

        return self.__class__.__name__ + ":{rec:%s, val:%s}" % (self.rec, vals)
