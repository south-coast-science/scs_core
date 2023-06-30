"""
Created on 8 Mar 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class ArrayDict(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, data=()):                    # data - array of key / value pairs
        """
        Constructor
        """
        self.__data = OrderedDict()

        for key, value in data:
            self.append(key, value)


    def __len__(self):
        return len(self.__data)


    def __contains__(self, key):
        return key in self.__data


    def __getitem__(self, key):
        return self.__data[key]                 # may raise KeyError


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, key, value):
        if key not in self.__data:
            self.__data[key] = []

        self.__data[key].append(value)


    # ----------------------------------------------------------------------------------------------------------------

    def get(self, key):
        try:
            return self.__data[key]
        except KeyError:
            return []


    def keys(self):
        return self.__data.keys()


    def values(self):
        return self.__data.values()


    def items(self):
        return self.__data.items()


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__data


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ArrayDict:{data:%s}" % Str.collection(self.__data)
