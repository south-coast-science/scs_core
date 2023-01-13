"""
Created on 13 Jan 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time


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
        self.__start_time = time.time()


    # ----------------------------------------------------------------------------------------------------------------

    def elapsed(self):
        return self.__start_time - time.time()


    def check(self):
        elapsed = self.elapsed()
        self.__start_time = time.time()

        return elapsed


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Timer:{start_time:%s}" % self.__start_time
