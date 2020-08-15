"""
Created on 14 Aug 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a non-threadsafe server
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
        self.__path = path                          # string
        self.__logger = logger                      # Logger

        self.__uds = DomainSocket(path)             # DomainSocket


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        try:
            os.remove(self.__path)              # override any previous use of the UDS
        except FileNotFoundError:
            pass

        self.__uds.connect()
        self.__uds.accept()

        self.__log('started')


    def stop(self):
        self.__uds.close()

        try:
            os.remove(self.__path)
        except FileNotFoundError:
            pass

        self.__log('stopped')


    def wait_for_request(self):
        while True:
            message = self.__uds.server_receive()

            if message != UDSClient.EOS:
                return message

            self.__log('restarting...')

            self.stop()                         # attempt to restart session
            self.start()


    def respond(self, message):
        self.__uds.server_send(message)


    # ----------------------------------------------------------------------------------------------------------------

    def __log(self, message):
        if not self.__logger:
            return

        self.__logger.info("UDSServer(%s): %s" % (self.__uds.path, message))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UDSServer:{uds:%s, logger=%s}" % (self.__uds, self.__logger)
