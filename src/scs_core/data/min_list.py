"""
Created on 19 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A tool to remove outlier (excessively low) minimum values
Note that we sort the list in order to minimise the number of required tests.
"""

from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class MinList(object):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, length):
        """
        Constructor
        """
        self.__length = length                  # int
        self.__minimums = []                    # array of comparable


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, value):
        mins_length = len(self.__minimums)

        if mins_length < self.__length:
            self.__minimums.append(value)
            self.__minimums.sort(reverse=True)
            return

        if value >= max(self.__minimums):
            return

        for i in range(mins_length):
            if value < self.__minimums[i]:
                self.__minimums[i] = value
                self.__minimums.sort(reverse=True)
                return


    def max_minimum(self):
        if not self.__minimums:
            return None

        return self.__minimums[0]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        minimums = Str.collection(self.__minimums)

        return "MinList:{length:%s, minimums:%s}" % (self.__length, minimums)
