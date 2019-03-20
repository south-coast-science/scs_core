"""
Created on 27 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class ProcessComms(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def connect(self, wait_for_availability=True):
        pass


    @abstractmethod
    def close(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def read(self):
        pass


    @abstractmethod
    def write(self, message, wait_for_availability=True):
        pass
