"""
Created on 13 Jan 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from time import time


# --------------------------------------------------------------------------------------------------------------------

class Timer(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__start_time = time()


    # ----------------------------------------------------------------------------------------------------------------

    def elapsed(self):
        elapsed = time() - self.__start_time

        return round(elapsed, 3)


    def check(self):
        elapsed = time() - self.__start_time
        self.__start_time = time()

        return round(elapsed, 3)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Timer:{start_time:%s}" % self.__start_time
