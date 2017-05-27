"""
Created on 27 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class ProcessComms(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def read(self):
        pass


    @abstractmethod
    def write(self, message, wait_for_availability=True):
        pass


    @abstractmethod
    def close(self):
        pass
