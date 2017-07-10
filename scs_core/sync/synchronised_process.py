"""
Created on 9 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.python.org/3/library/multiprocessing.html#sharing-state-between-processes
http://eli.thegreenplace.net/2012/01/04/shared-counter-with-pythons-multiprocessing/
"""

from abc import abstractmethod

from multiprocessing import Process, Lock


# --------------------------------------------------------------------------------------------------------------------

class SynchronisedProcess(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, value):
        """
        Constructor
        """
        self.__lock = Lock()
        self.__value = value


    # ----------------------------------------------------------------------------------------------------------------

    def start(self):
        proc = Process(target=self.run)
        proc.start()

        return proc


    @abstractmethod
    def run(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def value(self):
        with self._lock:
            return self.__value


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def _value(self):
        return self.__value


    @property
    def _lock(self):
        return self.__lock


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SynchronisedProcess:{value:%s}" % self.value
