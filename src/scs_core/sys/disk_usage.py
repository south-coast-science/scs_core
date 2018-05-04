"""
Created on 16 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

JSON example:
{"free": 61745299456, "total": 61749133312, "used": 3833856}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class DiskUsage(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        volume = jdict.get('volume')

        free = jdict.get('free')
        total = jdict.get('total')
        used = jdict.get('used')

        return DiskUsage(volume, free, total, used)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, volume, free, total, used):
        """
        Constructor
        """
        self.__volume = volume                      # string

        self.__free = int(free)                     # int
        self.__total = int(total)                   # int
        self.__used = int(used)                     # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['volume'] = self.volume

        jdict['free'] = self.free
        jdict['total'] = self.total
        jdict['used'] = self.used

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def volume(self):
        return self.__volume


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
        return "DiskUsage:{volume:%s, free:%s, total:%s, used:%s}" %  (self.volume, self.free, self.total, self.used)
