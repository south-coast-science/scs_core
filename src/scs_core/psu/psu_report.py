"""
Created on 13 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Defines the functionality and fields required by PSUMonitor
"""

from abc import ABC, abstractmethod

from scs_core.data.json import JSONReport


# --------------------------------------------------------------------------------------------------------------------

class PSUReport(JSONReport, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic
    def is_null_datum(self):
        return False


    @abstractmethod
    def below_power_threshold(self, charge_min):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def source(self):
        return None


    @property
    @abstractmethod
    def standby(self):
        return None


    @property
    @abstractmethod
    def input_power_present(self):
        return None


    @property
    @abstractmethod
    def v_in(self):
        return None


    @property
    @abstractmethod
    def batt_percent(self):
        return None


    @property
    @abstractmethod
    def charge_status(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def as_json(self):
        pass
