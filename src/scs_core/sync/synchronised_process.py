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

    def __init__(self, value=None):
        """
        Constructor
        """
        self.__proc = None
        self.__lock = Lock()
        self.__value = value


    # ----------------------------------------------------------------------------------------------------------------
    # process...

    def start(self):
        self.__proc = Process(target=self.run)
        self.__proc.start()


    def stop(self):
        if self.__proc is None:
            return

        self.__proc.terminate()
        self.__proc = None


    @abstractmethod
    def run(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def _proc(self):
        return self.__proc


    @property
    def _lock(self):
        return self.__lock


    @property
    def _value(self):
        return self.__value


    @_value.setter
    def _value(self, value):
        self.__value = value
