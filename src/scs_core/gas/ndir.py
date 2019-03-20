"""
Created on 15 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

The abstract definition of an NDIR required by NDIRMonitor.
Implementations are elsewhere.
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class NDIR(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    # abstract NDIR...

    @abstractmethod
    def power_on(self):
        pass


    @abstractmethod
    def power_off(self):
        pass


    @abstractmethod
    def sample(self):
        pass


    @abstractmethod
    def version(self):
        pass


    @abstractmethod
    def get_sample_interval(self):
        pass
