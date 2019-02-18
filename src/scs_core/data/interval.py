"""
Created on 16 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Interval(JSONable):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, prev_time, time, precision=3):
        diff = None if prev_time is None else round(time.timestamp() - prev_time.timestamp(), precision)

        return Interval(time, diff)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, time, diff):
        """
        Constructor
        """
        self.__time = time              # LocalizedDatetime
        self.__diff = diff              # float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['time'] = self.time.as_iso8601()
        jdict['diff'] = self.diff

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def time(self):
        return self.__time


    @property
    def diff(self):
        return self.__diff


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Interval:{time:%s, diff:%s}" % (self.time, self.diff)
