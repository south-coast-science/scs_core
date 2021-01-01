"""
Created on 22 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

If tally is None: computes the average of all the appended data.
If tally is a positive integer N: computes the average of the last N appended data.
"""

from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class Average(object):
    """
    classdocs
    """

    MIN_DATA_POINTS =   1

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tally=None):
        """
        Constructor
        """
        self.__tally = tally                            # number of rolling samples (None for all samples)
        self.__data = []


    def __len__(self):
        return len(self.__data)


    # ----------------------------------------------------------------------------------------------------------------

    def has_midpoint(self):
        return len(self.__data) > 0


    def has_tally(self):
        count = len(self)

        if self.__tally is None:
            return count >= self.MIN_DATA_POINTS

        return count >= self.__tally


    def append(self, value):
        count = len(self.__data)

        # remove oldest?
        if self.__tally is not None and count == self.__tally:
            del self.__data[0]

        # append...
        self.__data.append(value)


    def reset(self):
        self.__data = []


    # ----------------------------------------------------------------------------------------------------------------

    def mid(self, ndigits=None):
        count = len(self)

        if count < Average.MIN_DATA_POINTS:
            return None

        print("mid - data: %s" % Str.collection(self.__data))
        print("mid - sum: %s" % sum(self.__data))
        print("mid - len: %s" % len(self.__data))

        average = sum(self.__data) / len(self.__data)

        return average if ndigits is None else round(average, ndigits)


    # ----------------------------------------------------------------------------------------------------------------

    def min(self):
        return min(self.__data)


    def max(self):
        return max(self.__data)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Average:{tally:%s, items:%s}" % (self.__tally, len(self))
