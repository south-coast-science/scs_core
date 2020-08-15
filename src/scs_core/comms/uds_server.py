"""
Created on 14 Aug 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

supports single client only
"""

import os

from scs_core.comms.uds_client import UDSClient
from scs_host.comms.domain_socket import DomainSocket


# --------------------------------------------------------------------------------------------------------------------
# input reader...

class UDSServer(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, logger=None):
        """
        Constructor
        """
        self.__path = path
        self.__uds = DomainSocket(path, logger=logger)


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        try:
            os.remove(self.__path)              # override any previous use of the UDS
        except FileNotFoundError:
            pass

        self.__uds.connect()
        self.__uds.accept()


    def stop(self):
        self.__uds.close()

        try:
            os.remove(self.__path)
        except FileNotFoundError:
            pass


    def wait_for_request(self):
        while True:
            message = self.__uds.server_receive()

            if message != UDSClient.EOS:
                return message

            self.stop()                         # attempt to restart session
            self.start()


    def respond(self, message):
        self.__uds.server_send(message)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UDSServer:{uds:%s}" % self.__uds
