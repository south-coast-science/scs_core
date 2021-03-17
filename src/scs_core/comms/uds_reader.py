"""
Created on 13 Jul 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://realpython.com/python-sockets/#multi-connection-server
"""

import os
import sys


# --------------------------------------------------------------------------------------------------------------------
# input reader...

class UDSReader(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, socket, path):
        """
        Constructor
        """
        if path is None:
            self.__uds = None
            return

        try:
            os.remove(path)             # override any previous use of the UDS
        except OSError:
            pass

        self.__uds = socket(path)       # DomainSocket


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        if self.__uds:
            self.__uds.connect()


    def close(self):
        if self.__uds:
            self.__uds.close()


    def messages(self):
        if self.__uds:
            for message in self.__uds.read():
                yield message.strip()

        else:
            for message in sys.stdin:
                yield message.strip()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UDSReader:{uds:%s}" % self.__uds
