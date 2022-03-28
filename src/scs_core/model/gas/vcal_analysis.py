"""
Created on 27 Mar 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.stats import Stats


# --------------------------------------------------------------------------------------------------------------------

class VCalAnalysis(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        offset = jdict.get('offset')
        minimum = jdict.get('min')

        lower3 = jdict.get('l3')
        lower2 = jdict.get('l2')
        lower1 = jdict.get('l1')

        upper1 = jdict.get('u1')
        upper2 = jdict.get('u2')
        upper3 = jdict.get('u3')

        return cls(offset, minimum, lower3, lower2, lower1, upper1, upper2, upper3)


    @classmethod
    def construct(cls, offset, stats: Stats):
        return cls(offset, stats.minimum, stats.lower3(), stats.lower2(), stats.lower1(),
                   stats.upper1(), stats.upper2(), stats.upper3())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, offset, minimum, lower3, lower2, lower1, upper1, upper2, upper3):
        """
        Constructor
        """
        self.__offset = int(offset)
        self.__minimum = round(float(minimum), 1)

        self.__lower3 = round(float(lower3), 1)
        self.__lower2 = round(float(lower2), 1)
        self.__lower1 = round(float(lower1), 1)

        self.__upper1 = round(float(upper1), 1)
        self.__upper2 = round(float(upper2), 1)
        self.__upper3 = round(float(upper3), 1)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['offset'] = self.offset
        jdict['min'] = self.minimum

        jdict['l3'] = self.lower3
        jdict['l2'] = self.lower2
        jdict['l1'] = self.lower1

        jdict['u1'] = self.upper1
        jdict['u2'] = self.upper2
        jdict['u3'] = self.upper3

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def offset(self):
        return self.__offset


    @property
    def minimum(self):
        return self.__minimum


    @property
    def lower3(self):
        return self.__lower3


    @property
    def lower2(self):
        return self.__lower2


    @property
    def lower1(self):
        return self.__lower1


    @property
    def upper1(self):
        return self.__upper1


    @property
    def upper2(self):
        return self.__upper2


    @property
    def upper3(self):
        return self.__upper3


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "VCalAnalysis:{offset:%s, minimum:%s, lower3:%s, lower2:%s, lower1:%s, " \
               "upper1:%s, upper2:%s, upper3:%s}" % \
               (self.offset, self.minimum, self.lower3, self.lower2, self.lower1,
                self.upper1, self.upper2, self.upper3)
