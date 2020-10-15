"""
Created on 14 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

JSON example:
{"filesystem": "/dev/mmcblk0p1", "size": 15384184, "used": 319296, "free": 14892092,
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
        size = groups[1]
        used = groups[2]
        free = groups[3]
        mounted_on = groups[5]

        return cls(filesystem, size, used, free, mounted_on)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filesystem, size, used, free, mounted_on):
        """
        Constructor
        """
        self.__filesystem = filesystem                      # string
        self.__size = int(size)                             # int blocks
        self.__used = int(used)                             # int blocks
        self.__free = int(free)                             # int blocks
        self.__mounted_on = mounted_on                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['filesystem'] = self.filesystem
        jdict['size'] = self.size
        jdict['used'] = self.used
        jdict['free'] = self.free
        jdict['mounted-on'] = self.mounted_on

        jdict['is-available'] = self.is_available

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

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
    def size(self):
        return self.__size


    @property
    def used(self):
        return self.__used


    @property
    def free(self):
        return self.__free


    @property
    def mounted_on(self):
        return self.__mounted_on


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DiskVolume:{filesystem:%s, size:%s, used:%s, free:%s, mounted_on:%s}" %  \
               (self.filesystem, self.size, self.used, self.free, self.mounted_on)


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
        size = jdict.get('size')
        used = jdict.get('used')
        free = jdict.get('free')
        mounted_on = jdict.get('mounted-on')

        is_available = jdict.get('is-available')

        return cls(filesystem, size, used, free, mounted_on, is_available)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filesystem, size, used, free, mounted_on, is_available):
        """
        Constructor
        """
        super().__init__(filesystem, size, used, free, mounted_on)

        self.__is_available = is_available                  # bool


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def is_available(self):
        return self.__is_available


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ReportedDiskVolume:{filesystem:%s, size:%s, used:%s, free:%s, mounted_on:%s, is_available:%s}" %  \
               (self.filesystem, self.size, self.used, self.free, self.mounted_on, self.is_available)
