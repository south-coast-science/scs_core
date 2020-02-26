"""
Created on 4 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Node(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def name(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def ndir_spi_bus(self):
        pass


    @abstractmethod
    def ndir_spi_device(self):
        pass


    @abstractmethod
    def opc_spi_bus(self):
        pass


    @abstractmethod
    def opc_spi_device(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def disk_usage(self, volume):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def time_is_synchronized(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def home_dir(self):
        pass


    @abstractmethod
    def lock_dir(self):
        pass


    @abstractmethod
    def tmp_dir(self):
        pass


    @abstractmethod
    def command_dir(self):
        pass


    @abstractmethod
    def scs_dir(self):
        pass


    @abstractmethod
    def conf_dir(self):
        pass


    @abstractmethod
    def aws_dir(self):
        pass


    @abstractmethod
    def osio_dir(self):
        pass


    @abstractmethod
    def eep_image(self):
        pass


    @abstractmethod
    def software_update_report(self):
        pass

