"""
Created on 14 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

JSON example:
{"filesystem": "/dev/mmcblk0p1", "size": 15384184, "used": 319296, "available": 14892092, "use-percent": 3.0,
"mounted-on": "/srv/SCS_logging"}

https://stackoverflow.com/questions/35469685/in-python-how-do-i-get-a-list-of-all-partitions-in-mac-os-x
"""

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
        available = groups[3]
        use_percent = groups[4]

        mounted_on = groups[5]

        return cls(filesystem, size, used, available, use_percent, mounted_on)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        filesystem = jdict.get('filesystem')

        size = jdict.get('size')
        used = jdict.get('used')
        available = jdict.get('available')
        use_percent = jdict.get('use-percent')

        mounted_on = jdict.get('mounted-on')

        return cls(filesystem, size, used, available, use_percent, mounted_on)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filesystem, size, used, available, use_percent, mounted_on):
        """
        Constructor
        """
        self.__filesystem = filesystem                      # string

        self.__size = int(size)                             # int blocks
        self.__used = int(used)                             # int blocks
        self.__available = int(available)                   # int blocks
        self.__use_percent = float(use_percent)             # float %

        self.__mounted_on = mounted_on                      # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['filesystem'] = self.filesystem

        jdict['size'] = self.size
        jdict['used'] = self.used
        jdict['available'] = self.available
        jdict['use-percent'] = self.use_percent

        jdict['mounted-on'] = self.mounted_on

        return jdict


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
    def available(self):
        return self.__available


    @property
    def use_percent(self):
        return self.__use_percent


    @property
    def mounted_on(self):
        return self.__mounted_on


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DiskVolume:{filesystem:%s, size:%s, used:%s, available:%s, use_percent:%s, mounted_on:%s}" %  \
               (self.filesystem, self.size, self.used, self.available, self.use_percent, self.mounted_on)
