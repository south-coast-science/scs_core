"""
Created on 30 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Sampler(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, runner):
        """
        Constructor
        """
        self.__runner = runner


    # ----------------------------------------------------------------------------------------------------------------

    def reset(self):
        self.__runner.reset()


    def samples(self):
        for sample in self.__runner.samples(self):
            try:
                yield sample

            except (ConnectionError, StopIteration):
                break


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def sample(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def runner(self):
        return self.__runner
