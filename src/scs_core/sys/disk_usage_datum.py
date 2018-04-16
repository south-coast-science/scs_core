"""
Created on 16 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

http://code.activestate.com/recipes/577972-disk-usage/

JSON example:
{"time": "2017-05-29T12:40:58.619+01:00", "up": {"days": 1, "hours": 19, "minutes": 34, "seconds": 0},
"total": 0, "used": {"av1": 0.66, "av5": 0.65, "av15": 0.6}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class DiskUsageDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        free = jdict.get('free')
        total = jdict.get('total')
        used = jdict.get('used')

        return DiskUsageDatum(free, total, used)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, free, total, used):
        """
        Constructor
        """
        self.__free = int(free)                     # int
        self.__total = int(total)                   # int
        self.__used = int(used)                     # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['free'] = self.free
        jdict['total'] = self.total
        jdict['used'] = self.used

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def free(self):
        return self.__free


    @property
    def total(self):
        return self.__total


    @property
    def used(self):
        return self.__used


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DiskUsageDatum:{free:%s, total:%s, used:%s}" %  (self.free, self.total, self.used)


