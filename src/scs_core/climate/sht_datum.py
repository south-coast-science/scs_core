"""
Created on 18 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SHTDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        humid = jdict.get('hmd')
        temp = jdict.get('tmp')

        return cls(humid, temp)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, humid, temp):
        """
        Constructor
        """
        self.__humid = Datum.float(humid, 1)                # relative humidity       %
        self.__temp = Datum.float(temp, 1)                  # temperature             °C


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['hmd'] = self.humid
        jdict['tmp'] = self.temp

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def humid(self):
        return self.__humid


    @property
    def temp(self):
        return self.__temp


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SHTDatum:{humid:%0.1f, temp:%0.1f}" % (self.humid, self.temp)
