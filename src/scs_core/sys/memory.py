"""
Created on 14 Jan 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
"""

import os

from psutil import Process


# --------------------------------------------------------------------------------------------------------------------

class Memory(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__process = Process(os.getpid())
        self.__base_usage = self.__process.memory_info().rss


    # ----------------------------------------------------------------------------------------------------------------

    def total(self):
        usage = self.__process.memory_info().rss

        return int(round(usage / 1024))


    def heap(self):
        usage = self.__process.memory_info().rss - self.__base_usage

        return int(round(usage / 1024))


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Memory:{process:%s, base_usage:%s}" % (self.__process, self.__base_usage)
