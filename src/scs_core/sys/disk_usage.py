"""
Created on 16 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

JSON example:
{"volume": "/etc", "free": 2375217152, "used": 4958257152, "total": 7710990336}
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
        used = jdict.get('used')
        total = jdict.get('total')

        return DiskUsage(volume, free, used, total)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, volume, free, used, total):
        """
        Constructor
        """
        self.__volume = volume                      # string

        self.__free = int(free)                     # int
        self.__used = int(used)                     # int
        self.__total = int(total)                   # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['volume'] = self.volume

        jdict['free'] = self.free
        jdict['used'] = self.used
        jdict['total'] = self.total

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def volume(self):
        return self.__volume


    @property
    def free(self):
        return self.__free


    @property
    def used(self):
        return self.__used


    @property
    def total(self):
        return self.__total


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DiskUsage:{volume:%s, free:%s, used:%s, total:%s}" %  (self.volume, self.free, self.used, self.total)
