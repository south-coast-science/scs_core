"""
Created on 13 Jul 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://realpython.com/python-sockets/#multi-connection-server
"""

import sys


# --------------------------------------------------------------------------------------------------------------------

class UDSWriter(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, socket, path):
        """
        Constructor
        """
        self.__uds = socket(path) if path else None             # DomainSocket


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, wait_for_availability=True):
        if self.__uds:
            self.__uds.connect(wait_for_availability=wait_for_availability)


    def close(self):
        if self.__uds:
            self.__uds.close()


    def write(self, message, wait_for_availability=True):
        if self.__uds:
            self.__uds.write(message, wait_for_availability)

        else:
            print(message)
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__uds.path if self.__uds else None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UDSWriter:{uds:%s}" % self.__uds
