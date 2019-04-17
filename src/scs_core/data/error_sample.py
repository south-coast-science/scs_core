"""
Created on 16 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import statistics


# --------------------------------------------------------------------------------------------------------------------

class ErrorSample(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__reports = []                     # array of float
        self.__refs = []                        # array of float


    def __len__(self):
        return len(self.__reports)


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, report, ref):
        self.__reports.append(report)
        self.__refs.append(ref)


    # ----------------------------------------------------------------------------------------------------------------

    def lowest(self):
        errors = self.__errors()

        if not errors:
            return None

        return round(min(errors), 1)


    def highest(self):
        errors = self.__errors()

        if not errors:
            return None

        return round(max(errors), 1)


    def max(self):
        max_error = None

        for error in self.__errors():
            if max_error is None or abs(error) > abs(max_error):
                max_error = error

        return None if max_error is None else round(max_error, 1)


    def avg(self):
        errors = self.__errors()

        if not errors:
            return None

        return round(sum(errors) / len(errors), 1)


    def stdev(self):
        try:
            return round(statistics.stdev(self.__errors()), 3)

        except statistics.StatisticsError:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def __errors(self):
        return [self.__reports[i] - self.__refs[i] for i in range(len(self))]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorSample:{size:%s}" % len(self)
