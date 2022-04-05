"""
Created on 27 Mar 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

{"offset": -100, "NO2": {"min": 0.8, "max": 3.8, "l3": 0.5, "l2": 1.0, "l1": 1.5, "u1": 2.5, "u2": 3.0, "u3": 3.5},
"SO2": {"min": -0.7, "max": 12.9, "l3": -3.4, "l2": -0.7, "l1": 2.0, "u1": 7.4, "u2": 10.1, "u3": 12.8}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.stats import Stats


# --------------------------------------------------------------------------------------------------------------------

class VCalAnalyses(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        offset = None
        analyses = OrderedDict()

        for key, item in jdict.items():
            if key == 'offset':
                offset = item
                continue

            analyses[key] = VCalAnalysis.construct_from_jdict(item)

        return cls(offset, analyses)


    @classmethod
    def construct(cls, offset):
        return cls(offset, OrderedDict())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, offset, analyses):
        """
        Constructor
        """
        self.__offset = int(offset)
        self.__analyses = analyses                  # OrderedDict of gas: analysis



    # ----------------------------------------------------------------------------------------------------------------

    def append_stats(self, gas, jdict):
        self.__analyses[gas] = VCalAnalysis.construct_from_stats_jdict(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['offset'] = self.offset

        for gas, analysis in self.analyses.items():
            jdict[gas] = analysis

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def offset(self):
        return self.__offset


    @property
    def analyses(self):
        return self.__analyses


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "VCalAnalyses:{offset:%s, analyses:%s}" % (self.offset, self.analyses)


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

        minimum = jdict.get('min')
        maximum = jdict.get('max')

        lower3 = jdict.get('l3')
        lower2 = jdict.get('l2')
        lower1 = jdict.get('l1')

        upper1 = jdict.get('u1')
        upper2 = jdict.get('u2')
        upper3 = jdict.get('u3')

        amp1 = jdict.get('a1')
        amp2 = jdict.get('a2')
        amp3 = jdict.get('a3')

        return cls(minimum, maximum, lower3, lower2, lower1, upper1, upper2, upper3, amp1, amp2, amp3)


    @classmethod
    def construct_from_stats_jdict(cls, jdict):
        stats = Stats.construct_from_jdict(jdict)

        return cls(stats.minimum, stats.maximum, stats.lower3(), stats.lower2(), stats.lower1(),
                   stats.upper1(), stats.upper2(), stats.upper3(), stats.amp1(), stats.amp2(), stats.amp3())


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, minimum, maximum, lower3, lower2, lower1, upper1, upper2, upper3, amp1, amp2, amp3):
        """
        Constructor
        """
        self.__minimum = round(float(minimum), 1)
        self.__maximum = round(float(maximum), 1)

        self.__lower3 = round(float(lower3), 1)
        self.__lower2 = round(float(lower2), 1)
        self.__lower1 = round(float(lower1), 1)

        self.__upper1 = round(float(upper1), 1)
        self.__upper2 = round(float(upper2), 1)
        self.__upper3 = round(float(upper3), 1)

        self.__amp1 = round(float(amp1), 1)
        self.__amp2 = round(float(amp2), 1)
        self.__amp3 = round(float(amp3), 1)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['min'] = self.minimum
        jdict['max'] = self.maximum

        jdict['l3'] = self.lower3
        jdict['l2'] = self.lower2
        jdict['l1'] = self.lower1

        jdict['u1'] = self.upper1
        jdict['u2'] = self.upper2
        jdict['u3'] = self.upper3

        jdict['a1'] = self.amp1
        jdict['a2'] = self.amp2
        jdict['a3'] = self.amp3

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def minimum(self):
        return self.__minimum


    @property
    def maximum(self):
        return self.__maximum


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


    @property
    def amp1(self):
        return self.__amp1


    @property
    def amp2(self):
        return self.__amp2


    @property
    def amp3(self):
        return self.__amp3


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "VCalAnalysis:{minimum:%s, maximum:%s, lower3:%s, lower2:%s, lower1:%s, " \
               "upper1:%s, upper2:%s, upper3:%s, amp1:%s, amp2:%s, amp3:%s}" % \
               (self.minimum, self.maximum, self.lower3, self.lower2, self.lower1,
                self.upper1, self.upper2, self.upper3, self.amp1, self.amp2, self.amp3)
