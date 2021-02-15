"""
Created on 13 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An abstract PSU
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class PSU(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def name(cls):
        pass


    @classmethod
    @abstractmethod
    def requires_interface(cls):
        pass


    @classmethod
    @abstractmethod
    def uses_batt_pack(cls):
        pass


    @classmethod
    @abstractmethod
    def report_class(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def open(self):
        pass


    @abstractmethod
    def close(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def communicate(self, command):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def status(self):
        pass


    @abstractmethod
    def charge_min(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def version(self):
        pass


    @abstractmethod
    def uptime(self):
        pass


    @abstractmethod
    def host_shutdown_initiated(self):
        pass


    @abstractmethod
    def watchdog_start(self, interval):
        pass


    @abstractmethod
    def watchdog_stop(self):
        pass


    @abstractmethod
    def watchdog_touch(self):
        pass


    @abstractmethod
    def charge_pause(self, on):
        pass


    @abstractmethod
    def charge_dead(self, on):
        pass


    @abstractmethod
    def power_peripherals(self, on):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def batt_pack(self):
        pass
