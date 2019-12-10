"""
Created on 9 Dec 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

an abstract particulate exegesis model
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
        return host.conf_dir(), "particulate_exegete_" + cls.name() + "_calib.json"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def name(cls):
        pass


    @classmethod
    @abstractmethod
    def standard(cls):
        pass


    @classmethod
    @abstractmethod
    def uses_external_sht(cls):
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
    def interpret(self, text, rh):
        pass
