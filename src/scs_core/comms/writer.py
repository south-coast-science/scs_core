"""
Created on 23 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Writer(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def connect(self):
        pass


    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def write(self, message, wait_for_availability=False):
        pass
