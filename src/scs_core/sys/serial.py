"""
Created on 19 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/7266558/pyserial-buffer-wont-flush
"""

import time

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Serial(ABC):
    """
    classdocs
    """

    _DEFAULT_EOL = "\n"

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

    def read_lines(self, eol=None, timeout=None):
        while True:
            try:
                yield self.read_line(eol, timeout)

            except TimeoutError:
                return


    def read_line(self, eol=None, timeout=None):
        terminator = self._DEFAULT_EOL if eol is None else eol
        end_time = None if timeout is None else time.time() + timeout

        line = ""
        while True:
            if timeout is not None and time.time() > end_time:
                raise TimeoutError(timeout)

            char = self._ser.read().decode(errors='ignore')
            line += char

            if line.endswith(terminator):
                break

        return line.strip()


    def write_line(self, text, eol=None):
        terminator = self._DEFAULT_EOL if eol is None else eol

        text_ln = text.strip() + terminator
        packet = text_ln.encode()

        return self._ser.write(packet)


    # ----------------------------------------------------------------------------------------------------------------

    def read(self, count):
        chars = self._ser.read(count)

        return chars


    def write(self, *chars):
        self._ser.write(bytearray(chars))


    def flush_input(self):
        self._ser.flushInput()


    def flush_output(self):
        self._ser.flushOutput()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def port(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        is_open = False if self._ser is None else self._ser.is_open

        return self.__class__.__name__ + ":{port_number:%d, baud_rate=%d, hard_handshake=%s, serial_open:%s}" % \
            (self._port_number, self._baud_rate, self._hard_handshake, is_open)
