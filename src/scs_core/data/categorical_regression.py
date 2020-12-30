"""
Created on 11 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stats.idre.ucla.edu/spss/faq/coding-systems-for-categorical-variables-in-regression-analysis-2/
"""

from scs_core.data.regression import Regression


# --------------------------------------------------------------------------------------------------------------------

class CategoricalRegression(Regression):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__categories = set()


    def __len__(self):
        return len(self.__categories)


    # ----------------------------------------------------------------------------------------------------------------

    def has_midpoint(self):
        return len(self) > 0


    def has_regression(self):
        return len(self) > 0


    def append(self, _, value):
        self.__categories.add(value)


    def reset(self):
        self.__categories = set()


    # ----------------------------------------------------------------------------------------------------------------

    def midpoint(self, _ndigits=None):
        if len(self) != 1:
            return None, None

        return None, next(iter(self.__categories))


    # ----------------------------------------------------------------------------------------------------------------

    def min(self, _=None):
        if len(self) == 0:
            return None

        ordered = sorted(self.__categories)

        return ordered[0]


    def mid(self, _ndigits=None):
        if len(self) != 1:
            return None

        return next(iter(self.__categories))


    def max(self, _=None):
        if len(self) == 0:
            return None

        ordered = sorted(self.__categories)

        return ordered[-1]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CategoricalRegression:{categories:%s}" %  self.__categories
