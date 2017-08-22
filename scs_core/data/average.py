"""
Created on 22 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

If tally is None: computes the average of all the appended values.
If tally is a positive integer N: computes the average of the last N appended values.
"""


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
        self.__tally = tally
        self.__values = []


    # ----------------------------------------------------------------------------------------------------------------

    def has_tally(self):
        count = len(self.__values)

        if self.__tally is None:
            return count >= Average.MIN_DATA_POINTS

        return count >= self.__tally


    def append(self, value):
        count = len(self.__values)

        # remove oldest?
        if self.__tally is not None and count == self.__tally:
            del self.__values[0]

        # append...
        self.__values.append(float(value))


    def compute(self):
        count = len(self.__values)

        if count < Average.MIN_DATA_POINTS:
            return None

        total = 0

        for value in self.__values:
            total += value

        return total / count


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Average:{tally:%s, values:%s}" % (self.__tally, self.__values)


