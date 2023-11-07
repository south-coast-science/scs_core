"""
Created on 4 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
https://codereview.stackexchange.com/questions/101659/test-if-a-network-is-online-by-using-urllib2
"""

import platform
import re
import socket

from abc import ABC, abstractmethod
from collections import OrderedDict
from subprocess import Popen, DEVNULL, TimeoutExpired

from scs_core.sys.ipv4_address import IPv4Address


# --------------------------------------------------------------------------------------------------------------------

class Node(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    # network identity...

    @classmethod
    @abstractmethod
    def name(cls):
        pass


    @staticmethod
    def ipv4_address():
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        try:
            s.connect(('192.168.0.1', 1))           # host does not need to be reachable
            dot_decimal = s.getsockname()[0]

        except OSError:
            dot_decimal = '127.0.0.1'

        finally:
            s.close()

        return IPv4Address.construct(dot_decimal)


    @classmethod
    @abstractmethod
    def server_ipv4_address(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # scanner...

    @classmethod
    def scan_accessible_subnets(cls, start=1, end=254, ttl=32):
        for dot_decimal in cls.scan_subnet(cls.server_ipv4_address(), start=start, end=end, ttl=ttl):
            yield dot_decimal

        for dot_decimal in cls.scan_subnet(cls.ipv4_address(), start=start, end=end, ttl=ttl):
            yield dot_decimal


    @classmethod
    def scan_subnet(cls, ipv4_address, start=1, end=254, ttl=32):
        if ipv4_address is None:
            return

        pings = OrderedDict()

        # start...
        for addr in ipv4_address.lso_range(start, end):
            dot_decimal = addr.dot_decimal()
            pings[dot_decimal] = Popen(['ping', '-n', '-q', '-c', '1', '-t', str(ttl), dot_decimal],
                                       stdout=DEVNULL, stderr=DEVNULL)
        # report...
        for dot_decimal in pings:
            try:
                pings[dot_decimal].wait(timeout=ttl * 2.0)
            except (TimeoutExpired, TimeoutError):
                continue

            if pings[dot_decimal].returncode == 0:
                yield dot_decimal


    @staticmethod
    def ping(hostname, ttl=32):
        p = Popen(['ping', '-q', '-c', '1', '-t', str(ttl), hostname], stdout=DEVNULL, stderr=DEVNULL)
        p.wait()

        return p.returncode == 0


    @staticmethod
    def is_connected(hostname, timeout=None):
        try:
            socket.create_connection((hostname, 443)) if timeout is None else \
                socket.create_connection((hostname, 443), timeout=timeout)
            return True

        except OSError:
            return False


    # ----------------------------------------------------------------------------------------------------------------
    # software update...

    @abstractmethod
    def software_update_report(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # filesystem paths...

    @abstractmethod
    def home_path(self):
        pass


    @abstractmethod
    def scs_path(self):
        pass


# --------------------------------------------------------------------------------------------------------------------

class IoTNode(Node):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    # identity...

    @abstractmethod
    def hostname_prefix(self):
        pass


    @classmethod
    def numeric_component_of_name(cls):
        hostname = socket.gethostname()
        pieces = hostname.split('-')

        if len(pieces) != 3:
            raise ValueError(hostname)

        try:
            numeric_component = int(pieces[2])
        except ValueError:
            raise ValueError(hostname)

        return numeric_component


    # ----------------------------------------------------------------------------------------------------------------
    # version...

    @classmethod
    def has_acceptable_os_release(cls):
        minimum = cls.minimum_os_release().split('.')
        release = platform.uname().release

        match = re.match(r'^(\d+).(\d+).(\d+)-', release)

        if not match:
            raise ValueError(release)

        current = match.groups()

        for i in range(len(current)):
            if int(current[i]) > int(minimum[i]):
                return True

            if int(current[i]) < int(minimum[i]):
                return False

        return True


    @classmethod
    @abstractmethod
    def minimum_os_release(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # status...

    @abstractmethod
    def status(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # networks and modem...

    @classmethod
    @abstractmethod
    def networks(cls):
        pass


    @classmethod
    @abstractmethod
    def modem(cls):
        pass


    @classmethod
    @abstractmethod
    def modem_conn(cls):
        pass


    @classmethod
    @abstractmethod
    def sim(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # SPI...

    @abstractmethod
    def ndir_spi_dev_path(self):
        pass


    @abstractmethod
    def opc_spi_dev_path(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # time...

    @abstractmethod
    def time_is_synchronized(self):
        pass


    @abstractmethod
    def uptime(self, now=None):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # tmp directories...

    @abstractmethod
    def lock_dir(self):
        pass


    @abstractmethod
    def tmp_dir(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------
    # filesystem paths...

    @abstractmethod
    def command_path(self):
        pass


    @abstractmethod
    def eep_image(self):
        pass
