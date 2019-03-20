"""
Created on 1 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A device able to control a sampling process, by whatever method.
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Runner(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def reset(self):
        pass


    @abstractmethod
    def samples(self, sampler):
        pass
