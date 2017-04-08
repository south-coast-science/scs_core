"""
Created on 2 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
"derived-data": {
    "interval": 3600
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class DerivedData(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        interval = int(jdict.get('interval'))

        return DerivedData(interval)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interval):
        """
        Constructor
        """
        self.__interval = interval                          # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['interval'] = self.interval

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interval(self):
        return self.__interval


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DerivedData:{interval:%s}" % self.interval
