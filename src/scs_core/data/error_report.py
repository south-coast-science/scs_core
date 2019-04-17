"""
Created on 17 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ErrorReport(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, t_ts, rh_ts, stdev):
        """
        Constructor
        """
        self.__t_ts = t_ts                          # int
        self.__rh_ts = rh_ts                        # int
        self.__stdev = stdev                        # float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['t_ts'] = self.t_ts
        jdict['rh_ts'] = self.rh_ts
        jdict['stdev'] = self.stdev

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def t_ts(self):
        return self.__t_ts


    @property
    def rh_ts(self):
        return self.__rh_ts


    @property
    def stdev(self):
        return self.__stdev


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorReport:{t_ts:%s, rh_ts:%s, stdev:%s}" % (self.t_ts, self.rh_ts, self.stdev)
