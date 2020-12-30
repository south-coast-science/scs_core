"""
Created on 14 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod

from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class Regression(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def has_midpoint(self):
        pass


    @abstractmethod
    def has_regression(self):
        pass


    @abstractmethod
    def append(self, rec: LocalizedDatetime, value):
        pass


    @abstractmethod
    def reset(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def midpoint(self, ndigits=None):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def min(self, ndigits=None):
        pass


    @abstractmethod
    def mid(self, ndigits=None):
        pass


    @abstractmethod
    def max(self, ndigits=None):
        pass
