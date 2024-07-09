"""
Created on 19 Jun 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Median Absolute Percent Error (MdAPE)

https://www.geeksforgeeks.org/how-to-calculate-mape-in-python/ (MAPE)
https://stackoverflow.com/questions/24101524/finding-median-of-list-in-python (MdAPE)

https://www.isobudgets.com/7-steps-to-calculate-measurement-uncertainty/
"""

import statistics


# --------------------------------------------------------------------------------------------------------------------

class MdAPE(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, precision=3):
        """
        Constructor
        """
        self.__precision = int(precision)                       # int
        self.__apes = []                                        # array of float


    def __len__(self):
        return len(self.__apes)


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, reference, predicted):
        ape = abs((reference - predicted) / reference) * 100
        self.__apes.append(ape)

        return round(ape, self.__precision)


    def mdape(self):
        mdape = statistics.median(self.__apes)

        return round(mdape, self.__precision)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def apes(self):
        return self.__apes


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MdAPE:{precision:%s, apes:%s}" % (self.__precision, len(self))
