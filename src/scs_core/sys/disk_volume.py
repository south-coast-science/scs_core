"""
Created on 14 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

JSON example:
{"filesystem": "/dev/mmcblk0p1", "total": 15384184, "used": 319296, "free": 14892092,
"mounted-on": "/srv/SCS_logging", "is-available": false}

https://stackoverflow.com/questions/35469685/in-python-how-do-i-get-a-list-of-all-partitions-in-mac-os-x
"""

import os
import re

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class DiskVolume(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_df_row(cls, row):
        match = re.search(r'([^ ]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)%\s+([^ ]+)', row)

        if match is None:
            return None

        groups = match.groups()

        filesystem = groups[0]
        total = groups[1]
        used = groups[2]
        free = groups[3]
        mounted_on = groups[5]

        return cls(filesystem, free, used, total, mounted_on)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filesystem, free, used, total, mounted_on):
        """
        Constructor
        """
        self.__filesystem = filesystem                      # string
        self.__total = int(total)                           # int blocks
        self.__used = int(used)                             # int blocks
        self.__free = int(free)                             # int blocks
        self.__mounted_on = mounted_on                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['filesystem'] = self.filesystem
        jdict['free'] = self.free
        jdict['used'] = self.used
        jdict['total'] = self.total
        jdict['mounted-on'] = self.mounted_on

        jdict['is-available'] = self.is_available

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def percent_used(self):
        if not self.is_available:
            return None

        percent = self.used / self.total * 100

        return round(percent, 1)


    @property
    def is_available(self):
        try:
            os.listdir(self.mounted_on)
            return True

        except OSError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def filesystem(self):
        return self.__filesystem


    @property
    def free(self):
        return self.__free


    @property
    def used(self):
        return self.__used


    @property
    def total(self):
        return self.__total


    @property
    def mounted_on(self):
        return self.__mounted_on


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DiskVolume:{filesystem:%s, free:%s, used:%s, total:%s, mounted_on:%s}" %  \
               (self.filesystem, self.free, self.used, self.total, self.mounted_on)


# --------------------------------------------------------------------------------------------------------------------

class ReportedDiskVolume(DiskVolume):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        filesystem = jdict.get('filesystem')
        free = jdict.get('free')
        used = jdict.get('used')
        total = jdict.get('total')
        mounted_on = jdict.get('mounted-on')

        is_available = jdict.get('is-available')

        return cls(filesystem, free, used, total, mounted_on, is_available)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filesystem, free, used, total, mounted_on, is_available):
        """
        Constructor
        """
        super().__init__(filesystem, free, used, total, mounted_on)

        self.__is_available = is_available                  # bool


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_available(self):
        return self.__is_available


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ReportedDiskVolume:{filesystem:%s, free:%s, used:%s, total:%s, mounted_on:%s, is_available:%s}" %  \
               (self.filesystem, self.free, self.used, self.total, self.mounted_on, self.is_available)
