"""
Created on 14 Aug 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class UDSClient(object):
    """
    classdocs
    """

    EOS = 'UDS-CLIENT-EOS'                          # end of session message

    _RECONNECT_WAIT = 10.0                          # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, socket, path):
        """
        Constructor
        """
        self.__logger = Logging.getLogger()

        self.__path = path                          # string

        self.__uds = socket(path)                   # DomainSocket
        self.__disconnecting = False                # bool


    # ----------------------------------------------------------------------------------------------------------------

    def request(self, message):
        reported_waiting = False

        while True:
            try:
                self.__uds.client_send(message.strip())
                return

            except (BrokenPipeError, OSError):
                if self.__disconnecting:
                    return                          # don't wait forever if terminating

                if not reported_waiting:
                    self.__logger.info('waiting for server')
                    reported_waiting = True

                time.sleep(self._RECONNECT_WAIT)

                self.__uds.close()                  # attempt to restart session
                self.__uds.connect()


    def wait_for_response(self):
        return self.__uds.client_receive()


    # ----------------------------------------------------------------------------------------------------------------

    def open(self):
        self.__disconnecting = False
        self.__uds.connect()

        self.__logger.info('opened UDS')


    def close(self):
        self.__disconnecting = True
        self.request(self.EOS)
        self.__uds.close()

        self.__logger.info('closed UDS')


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UDSClient:{uds:%s}" % self.__uds
