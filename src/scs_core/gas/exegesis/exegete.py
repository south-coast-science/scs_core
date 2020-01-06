"""
Created on 17 Dec 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an abstract electrochem exegesis model
"""

from abc import ABC, abstractmethod

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Exegete(PersistentJSONable, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), "gas_exegete_" + cls.name() + "_calib.json"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def name(cls):
        pass


    @classmethod
    @abstractmethod
    def standard(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def __eq__(self, other):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def tag(self):
        if self == self.standard():
            return self.name()

        return self.name() + '?'                            # indicates non-standard coefficients


    @abstractmethod
    def error(self, t, rh):
        pass


    @abstractmethod
    def interpretation(self, text, t, rh):
        pass
