"""
Created on 23 Aug 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract LED controller.
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class LED(ABC):
    """
    classdocs
    """
    STATES = {'0': 0x00, 'R': 0x01, 'A': 0x03, 'G': 0x02}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_colour(cls, colour):
        return colour in cls.STATES


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def colour(self):
        pass


    @colour.setter
    @abstractmethod
    def colour(self, colour):
        pass
