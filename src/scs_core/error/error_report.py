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

    def __init__(self, t_ts, rh_ts, r2):
        """
        Constructor
        """
        self.__t_ts = t_ts                          # int
        self.__rh_ts = rh_ts                        # int
        self.__r2 = r2                              # float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['t_ts'] = self.t_ts
        jdict['rh_ts'] = self.rh_ts
        jdict['r2'] = round(self.r2, 3)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def t_ts(self):
        return self.__t_ts


    @property
    def rh_ts(self):
        return self.__rh_ts


    @property
    def r2(self):
        return self.__r2


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorReport:{t_ts:%s, rh_ts:%s, r2:%s}" % (self.t_ts, self.rh_ts, self.r2)
