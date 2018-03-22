"""
Created on 20 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Median filter
https://en.wikipedia.org/wiki/Median_filter
"""


# --------------------------------------------------------------------------------------------------------------------

class MedianFilter(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, window_size):
        """
        Constructor
        """
        if window_size % 2 == 0:
            raise ValueError("window_size must be an odd number")

        self.__window_size = window_size

        self.__window_midpoint = window_size // 2
        self.__window_index = 0
        self.__values = []


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, x):
        self.__values.append(x)

        # window is full...
        if self.__window_index == self.__window_size:
            self.__values.pop(0)

            sorted_values = sorted(self.__values)
            return sorted_values[self.__window_midpoint]

        # window is not full...
        self.__window_index += 1

        return x


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MedianFilter:{window_size:%s, window_midpoint:%s, window_index:%s, values:%s}" % \
               (self.__window_size, self.__window_midpoint, self.__window_index, self.__values)
