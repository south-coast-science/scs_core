"""
Created on 19 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Serial(ABC):
    """
    classdocs
    """

    EOL =               "\r\n"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, port_number, baud_rate, hard_handshake=False):
        """
        Constructor
        """
        self._port_number = port_number
        self._baud_rate = baud_rate
        self._hard_handshake = hard_handshake

        self._ser = None


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def open(self, lock_timeout, comms_timeout):
        pass


    @abstractmethod
    def close(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def read_line(self, eol, timeout):
        end_time = time.time() + timeout

        line = ""
        while True:
            if time.time() > end_time:
                break

            char = self._ser.read().decode(errors='ignore')
            line += char

            if line.endswith(eol):
                break

        return line.strip()


    def write_line(self, text, eol=None):
        terminator = self.EOL if eol is None else eol

        text_ln = text.strip() + terminator
        packet = text_ln.encode()

        return self._ser.write(packet)


    # ----------------------------------------------------------------------------------------------------------------

    def read(self, count):
        chars = self._ser.read(count)

        return chars


    def write(self, *chars):
        self._ser.write(bytearray(chars))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Serial:{port_number:%d, baud_rate=%d, hard_handshake=%s, serial:%s}" % \
               (self._port_number, self._baud_rate, self._hard_handshake, self._ser)
