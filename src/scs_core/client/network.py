"""
Created on 27 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import time

from abc import ABC
from multiprocessing import Process
from subprocess import Popen


# --------------------------------------------------------------------------------------------------------------------

class Network(ABC):
    """
    classdocs
    """
    __TEST_RESOURCE =       'google.com'
    __NETWORK_WAIT_TIME =   5.0                         # seconds


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def resource_is_available(resource):
        with open(os.devnull, 'wb') as devnull:
            return Popen(['ping', '-c', '1', resource], stdout=devnull, stderr=devnull).wait() == 0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_available(cls):
        return cls.resource_is_available(cls.__TEST_RESOURCE)


    @classmethod
    def wait(cls):
        cls.wait_for_resource(cls.__TEST_RESOURCE)


    @classmethod
    def wait_for_resource(cls, resource):
        while not cls.resource_is_available(resource):
            time.sleep(cls.__NETWORK_WAIT_TIME)


# ----------------------------------------------------------------------------------------------------------------

class NetworkMonitor(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interval, network_unavailable_handler):
        self.__interval = interval                                                  # float seconds
        self.__network_unavailable_handler = network_unavailable_handler            # function

        self.__proc = None                                                          # Process


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        self.__proc = Process(target=self.run)
        self.__proc.start()


    def run(self):
        try:
            Network.wait()

            while True:
                if not Network.is_available():
                    self.__network_unavailable_handler()

                time.sleep(self.__interval)

        except KeyboardInterrupt:
            pass


    def join(self):
        self.__proc.join()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NetworkMonitor:{interval:%s, network_unavailable_handler:%s, proc:%s}" % \
               (self.__interval, self.__network_unavailable_handler, self.__proc)

