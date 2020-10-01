"""
Created on 15 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alphasense A4 IRC-AT non-dispersive infra-red detector

The abstract definition of an NDIR required by NDIRMonitor.
Implementations are elsewhere.
"""

import time

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class NDIR(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def boot_time(cls):
        pass

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface):
        """
        Constructor
        """
        self.__interface = interface


    # ----------------------------------------------------------------------------------------------------------------

    def power_on(self):
        # print("ndir: power_on")

        self.__interface.power_ndir(True)
        time.sleep(self.boot_time())


    def power_off(self):
        # print("ndir: power_off")

        self.__interface.power_ndir(False)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interface(self):
        return self.__interface


    # ----------------------------------------------------------------------------------------------------------------
    # abstract NDIR...

    @abstractmethod
    def sample(self):
        pass


    @abstractmethod
    def version(self):
        pass


    @abstractmethod
    def get_sample_interval(self):
        pass
