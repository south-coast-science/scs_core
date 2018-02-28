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

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, *values):
        """
        Constructor
        """
        self.__tag = tag                        # string
        self.__rec = rec                        # LocalizedDatetime
        self.__val = OrderedDict(values)        # OrderedDict of (src, JSONable)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.tag is not None:
            jdict['tag'] = self.tag

        jdict['rec'] = self.rec.as_json()
        jdict['val'] = self.val

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def tag(self):
        return self.__tag


    @property
    def rec(self):
        return self.__rec


    @property
    def val(self):
        return self.__val


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        vals = '[' + ', '.join(str(key) + ': ' + str(self.val[key]) for key in self.val) + ']'

        return self.__class__.__name__ + ":{tag:%s, rec:%s, val:%s}" % (self.tag, self.rec, vals)
