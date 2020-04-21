"""
Created on 14 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from decimal import Decimal
from statistics import mean

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.regression import Regression


# --------------------------------------------------------------------------------------------------------------------

class LinearRegression(Regression):
    """
    classdocs
    """

    MIN_DATA_POINTS =   2

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tally=None, time_relative=False):
        """
        Constructor
        """
        self.__tally = tally                            # number of rolling samples (None for all samples)
        self.__time_relative = time_relative            # set first timestamp to time zero

        self.__start_timestamp = None
        self.__tzinfo = None
        self.__data = []


    def __len__(self):
        return len(self.__data)


    # ----------------------------------------------------------------------------------------------------------------

    def has_midpoint(self):
        return len(self) > 0


    def has_regression(self):
        return len(self) >= self.MIN_DATA_POINTS


    def append(self, rec: LocalizedDatetime, value):
        count = len(self)

        if count == 0:
            self.__start_timestamp = rec.timestamp()

        timestamp = rec.timestamp() - self.__start_timestamp if self.__time_relative else rec.timestamp()

        # remove oldest?
        if self.__tally is not None and count == self.__tally:
            del self.__data[0]

        # append...
        self.__data.append((Decimal(timestamp), Decimal(value)))

        self.__tzinfo = rec.tzinfo


    def reset(self):
        self.__start_timestamp = None
        self.__tzinfo = None
        self.__data = []


    # ----------------------------------------------------------------------------------------------------------------

    def line(self):
        # validate...
        if not self.has_regression():
            return None, None

        n = len(self)

        # init...
        sum_x = Decimal(0.0)
        sum_y = Decimal(0.0)

        sum_x2 = Decimal(0.0)
        sum_xy = Decimal(0.0)

        # sum....
        for x, y in self.__data:
            sum_x += x
            sum_y += y

            sum_x2 += x * x
            sum_xy += x * y

        # compute...
        avg_x = sum_x / n
        avg_y = sum_y / n

        d_x = (sum_x2 * n) - (sum_x * sum_x)
        d_y = (sum_xy * n) - (sum_x * sum_y)

        slope = d_y / d_x                                   # raises decimal.InvalidOperation if d_x is zero

        intercept = avg_y - (slope * avg_x)

        return float(slope), float(intercept)


    def midpoint(self, ndigits=None):
        # validate...
        if not self.has_midpoint():
            return None, None

        # single value...
        if len(self) == 1:
            for timestamp, value in self.__data:
                return LocalizedDatetime.construct_from_timestamp(timestamp, self.__tzinfo), float(value)

        # multiple values...
        slope, intercept = self.line()

        # x domain...
        x_data = [x for x, _ in self.__data]

        min_x = min(x_data)
        max_x = max(x_data)

        mid_x = mean((min_x, max_x))

        rec = LocalizedDatetime.construct_from_timestamp(mid_x, self.__tzinfo)

        # y val...
        value = slope * float(mid_x) + intercept

        return rec, value if ndigits is None else round(value, ndigits)


    # ----------------------------------------------------------------------------------------------------------------

    def min(self, ndigits=None):
        value = float(min([y for _, y in self.__data]))

        return value if ndigits is None else round(value, ndigits)


    def max(self, ndigits=None):
        value = float(max([y for _, y in self.__data]))

        return value if ndigits is None else round(value, ndigits)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LinearRegression:{tally:%s, time_relative:%s, start_timestamp:%s, tzinfo:%s, data:%s}" % \
               (self.__tally, self.__time_relative, self.__start_timestamp, self.__tzinfo, self.__data)
