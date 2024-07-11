"""
Created on 10 Jun 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Used to convert compact device tag representations (scs-opc-1) to text-sortable representations (scs-opc-0001).
"""

import re

from abc import ABC

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class SortableTag(JSONable, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

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


# --------------------------------------------------------------------------------------------------------------------

class UnstructuredTag(SortableTag):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name):
        """
        Constructor
        """
        self.__name = name                              # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.__name

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UnstructuredTag:{name:%s}" % self.__name


# --------------------------------------------------------------------------------------------------------------------

class DeviceTag(SortableTag):
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
            return UnstructuredTag(jdict)

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


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, sortable=False, **kwargs):
        serial = "%04d" % self.__serial if sortable else "%d" % self.__serial
        return str('-'.join((self.__vendor, self.__model, serial)))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceTag:{vendor:%s, model:%s, serial:%s}" % (self.__vendor, self.__model, self.__serial)
