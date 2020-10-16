"""
Created on 16 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

JSON example:
{"path": "/srv/removable_data_storage", "free": 15423610880, "used": 329793536, "total": 15753404416,
"is-available": true}

https://www.geeksforgeeks.org/python-os-statvfs-method/
"""

import os

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class DiskUsage(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_statvfs(cls, path, statvfs):
        free = statvfs.f_bfree * statvfs.f_bsize
        total = statvfs.f_blocks * statvfs.f_bsize
        used = total - free

        return cls(path, free, used, total)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, free, used, total):
        """
        Constructor
        """
        self.__path = path                          # string

        self.__free = int(free)                     # int bytes
        self.__used = int(used)                     # int bytes
        self.__total = int(total)                   # int bytes


    # ----------------------------------------------------------------------------------------------------------------

    def percent_used(self):
        if not self.is_available:
            return None

        percent = self.used / self.total * 100

        return round(percent, 1)


    @property
    def is_available(self):
        try:
            os.listdir(self.path)
            return True

        except OSError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['path'] = self.path

        jdict['free'] = self.free
        jdict['used'] = self.used
        jdict['total'] = self.total

        jdict['is-available'] = self.is_available

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


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
        return "DiskUsage:{path:%s, free:%s, used:%s, total:%s}" %  \
               (self.path, self.free, self.used, self.total)


# --------------------------------------------------------------------------------------------------------------------

class ReportedDiskUsage(DiskUsage):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        path = jdict.get('path')

        free = jdict.get('free')
        used = jdict.get('used')
        total = jdict.get('total')

        is_available = jdict.get('is-available')

        return cls(path, free, used, total, is_available)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, free, used, total, is_available):
        """
        Constructor
        """
        super().__init__(path, free, used, total)

        self.__is_available = is_available                      # bool


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_available(self):
        return self.__is_available


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ReportedDiskUsage:{path:%s, free:%s, used:%s, total:%s, is_available:%s}" %  \
               (self.path, self.free, self.used, self.total, self.is_available)
