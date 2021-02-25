"""
Created on 14 Aug 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a non-threadsafe server
"""

import os

from scs_core.sys.logging import Logging

from scs_core.comms.uds_client import UDSClient
from scs_host.comms.domain_socket import DomainSocket


# --------------------------------------------------------------------------------------------------------------------

class UDSServer(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path):
        """
        Constructor
        """
        self.__logger = Logging.getLogger()

        self.__path = path                          # string
        self.__uds = DomainSocket(path)             # DomainSocket


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        try:
            os.remove(self.__path)                  # override any previous use of the UDS
        except FileNotFoundError:
            pass

        self.__uds.connect()
        self.__uds.accept()

        self.__logger.info('started')


    def stop(self):
        self.__uds.close()

        try:
            os.remove(self.__path)
        except FileNotFoundError:
            pass

        self.__logger.info('stopped')


    def restart(self):
        self.__logger.info('restart...')

        self.stop()
        self.start()


    # ----------------------------------------------------------------------------------------------------------------

    def requests(self):
        while True:
            message = self.__uds.server_receive()

            if message != UDSClient.EOS:
                yield message
                continue

            self.restart()


    def respond(self, message):
        try:
            self.__uds.server_send(message.strip())

        except BrokenPipeError:
            self.restart()



    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UDSServer:{uds:%s}" % self.__uds
