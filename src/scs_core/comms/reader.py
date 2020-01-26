"""
Created on 23 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Reader(ABC):
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
    def messages(self):
        pass
