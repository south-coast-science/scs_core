"""
Created on 25 Jan 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PMxRequest(ABC, JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def is_compatible(self, group):
        pass


    @abstractmethod
    def is_zero(self):
        pass
