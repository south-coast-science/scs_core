"""
Created on 14 Aug 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.comms.domain_socket import DomainSocket


# --------------------------------------------------------------------------------------------------------------------

class UDSClient(object):
    """
    classdocs
    """

    EOS = 'UDS-CLIENT-EOS'                          # end of session message

    _RECONNECT_WAIT = 10.0                          # seconds

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, logger=None):
        """
        Constructor
        """
        self.__path = path                          # string
        self.__logger = logger                      # Logger

        self.__uds = DomainSocket(path)             # DomainSocket
        self.__disconnecting = False                # bool


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        self.__disconnecting = False
        self.__uds.connect()

        self.__log('connected')


    def disconnect(self):
        self.__disconnecting = True
        self.request(self.EOS)
        self.__uds.close()

        self.__log('disconnected')


    # ----------------------------------------------------------------------------------------------------------------

    def request(self, message):
        while True:
            try:
                self.__uds.client_send(message.strip())
                return

            except (BrokenPipeError, OSError):
                if self.__disconnecting:
                    return                          # don't wait forever if terminating

                time.sleep(self._RECONNECT_WAIT)

                self.__log('attempting reconnection')

                self.__uds.close()                  # attempt to restart session
                self.__uds.connect()


    def wait_for_response(self):
        return self.__uds.client_receive()


    # ----------------------------------------------------------------------------------------------------------------

    def __log(self, message):
        if not self.__logger:
            return

        self.__logger.info("UDSClient(%s): %s" % (self.__uds.path, message))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UDSClient:{uds:%s}" % self.__uds
