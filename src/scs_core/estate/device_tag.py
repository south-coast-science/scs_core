"""
Created on 10 Jun 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

examples:
scs-opc-1
scs-opc-0001
"""

import re

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class DeviceTag(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid(cls, tag):
        try:
            cls.construct_from_jdict(tag)
        except ValueError:
            return False

        return True


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        match = re.match(r'([a-z\d]+)-([a-z\d]+)-(\d+)', jdict)

        if not match:
            return None             # TODO: consider returning the string (and handling EQ cases, etc.)

        groups = match.groups()

        return cls(groups[0], groups[1], groups[2])


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, vendor, model, serial):
        """
        Constructor
        """
        self.__vendor = vendor                          # string
        self.__model = model                            # string
        self.__serial = int(serial)                     # int


    def __eq__(self, other):
        try:
            return self.as_json(sortable=True) == other.as_json(sortable=True)

        except (TypeError, AttributeError):
            return False


    def __gt__(self, other):
        return self.as_json(sortable=True) > other.as_json(sortable=True)


    def __lt__(self, other):
        return self.as_json(sortable=True) < other.as_json(sortable=True)


    def __hash__(self):
        return hash(self.as_json())


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, sortable=False, **kwargs):
        serial = "%04d" % self.serial if sortable else "%d" % self.serial
        return str('-'.join((self.vendor, self.model, serial)))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def vendor(self):
        return self.__vendor


    @property
    def model(self):
        return self.__model


    @property
    def serial(self):
        return self.__serial


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceTag:{vendor:%s, model:%s, serial:%s}" % (self.vendor, self.model, self.serial)
