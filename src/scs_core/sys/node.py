"""
Created on 4 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
"""

import socket

from abc import ABC, abstractmethod
from collections import OrderedDict
from subprocess import Popen, DEVNULL

from scs_core.sys.ipv4_address import IPv4Address


# --------------------------------------------------------------------------------------------------------------------

class Node(ABC):
    """
    classdocs
    """

    @classmethod
    def scan(cls, start, end):
        pings = OrderedDict()

        # start...
        for addr in cls.ipv4_address().lso_range(start, end):
            dot_decimal = addr.dot_decimal()
            pings[dot_decimal] = Popen(['ping', '-n', '-q', '-c', '1', '-t', '1', dot_decimal],
                                       stdout=DEVNULL, stderr=DEVNULL)
        # wait...
        for dot_decimal in pings:
            pings[dot_decimal].wait()

            if pings[dot_decimal].returncode == 0:
                yield dot_decimal


    @staticmethod
    def ping(host):
        p = Popen(['ping', '-q', '-c', '1', '-t', '1', host], stdout=DEVNULL, stderr=DEVNULL)
        p.wait()

        return p.returncode == 0


    @staticmethod
    def ipv4_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            s.connect(('192.168.0.1', 1))               # host does not need to be reachable
            dot_decimal = s.getsockname()[0]

        except OSError:
            dot_decimal = '127.0.0.1'

        finally:
            s.close()

        return IPv4Address.construct(dot_decimal)


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

