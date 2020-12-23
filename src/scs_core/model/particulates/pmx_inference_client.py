"""
Created on 23 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class PMxInferenceClient(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_client):
        """
        Constructor
        """
        self.__uds_client = uds_client                      # UDSClient


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self):
        self.__uds_client.connect()


    def disconnect(self):
        self.__uds_client.disconnect()


    @abstractmethod
    def infer(self, opc_sample, ext_sht_sample):
        pass
