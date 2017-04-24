"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class AFEDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pt1000, *sns):
        """
        Constructor
        """
        self.__pt1000 = pt1000
        self.__sns = OrderedDict(sns)   # None if sns is None else OrderedDict(sns)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pt1'] = self.pt1000
        jdict['sns'] = self.sns

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pt1000(self):
        return self.__pt1000


    @property
    def sns(self):
        return self.__sns


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        sns = '[' + ', '.join(str(key) + ':' + str(self.sns[key]) for key in self.sns) + ']'

        return "AFEDatum:{pt1000:%s, sns:{%s}}" % (self.pt1000, sns)
