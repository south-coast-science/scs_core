"""
Created on 27 Mar 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

{"offset": -100, "NO2": {"min": 0.8, "max": 3.8, "l3": 0.5, "l2": 1.0, "l1": 1.5, "u1": 2.5, "u2": 3.0, "u3": 3.5},
"SO2": {"min": -0.7, "max": 12.9, "l3": -3.4, "l2": -0.7, "l1": 2.0, "u1": 7.4, "u2": 10.1, "u3": 12.8}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.stats import StatsAnalysis


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

            analyses[key] = StatsAnalysis.construct_from_jdict(item)

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
        self.__analyses[gas] = StatsAnalysis.construct_from_stats_jdict(jdict)


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
