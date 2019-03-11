"""
Created on 11 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.regression import Regression


# --------------------------------------------------------------------------------------------------------------------

class CatagoricalRegression(Regression):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__data = set()


    def __len__(self):
        return len(self.__data)


    # ----------------------------------------------------------------------------------------------------------------

    def has_midpoint(self):
        return len(self) > 0


    def has_regression(self):
        return len(self) > 0


    def append(self, _, value):
        self.__data.add(value)


    def reset(self):
        self.__data = set()


    # ----------------------------------------------------------------------------------------------------------------

    def midpoint(self, ndigits=None):
        if len(self) != 1:
            return None, None

        return None, next(iter(self.__data))


    # ----------------------------------------------------------------------------------------------------------------

    def min(self, ndigits=None):
        ordered = sorted(self.__data)

        return ordered[0]


    def max(self, ndigits=None):
        ordered = sorted(self.__data)

        return ordered[-1]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CatagoricalRegression:{data:%s}" %  self.__data
