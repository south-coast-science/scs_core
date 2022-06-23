"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.str import Str


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
        self.__sns = OrderedDict(sns)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['src'] = 'AFE'

        if self.pt1000:
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


    @sns.setter
    def sns(self, sns):
        self.__sns = sns


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AFEDatum:{pt1000:%s, sns:%s}" % (self.pt1000, Str.collection(self.sns))
