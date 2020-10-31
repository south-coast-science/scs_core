"""
Created on 31 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class CalibCurrency(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rec = jdict.get('rec')
        delta = jdict.get('calib-delta')

        return cls(rec, delta)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, delta):
        """
        Constructor
        """
        self.__rec = rec                                    # LocalisedDatetime
        self.__delta = int(delta)                           # int seconds


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec
        jdict['calib-delta'] = self.delta

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def delta(self):
        return self.__delta


    @property
    def timedelta(self):
        return Timedelta(seconds=self.delta)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CalibCurrency:{rec:%s, delta:%s}" % (self.rec, self.delta)
