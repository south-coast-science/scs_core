"""
Created on 14 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class LinearRegression(object):
    """
    classdocs
    """

    MIN_DATA_POINTS =   2

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tally=None):
        """
        Constructor
        """
        self.__tally = tally
        self.__data = []


    def __len__(self):
        return len(self.__data)


    # ----------------------------------------------------------------------------------------------------------------

    def has_tally(self):
        count = len(self)

        if self.__tally is None:
            return count >= self.MIN_DATA_POINTS

        return count >= self.__tally


    def append(self, rec: LocalizedDatetime, value):
        count = len(self.__data)

        # remove oldest?
        if self.__tally is not None and count == self.__tally:
            del self.__data[0]

        # append...
        self.__data.append((rec.timestamp(), value))


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self):
        n = len(self)

        # validate...
        if n < self.MIN_DATA_POINTS:
            return None, None

        # init...
        sum_x = 0
        sum_y = 0

        sum_x2 = 0
        sum_xy = 0

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

        slope = d_y / d_x
        intercept = avg_y - (slope * avg_x)

        return slope, intercept


    def midpoint(self):
        slope, intercept = self.compute()

        # validate...
        if slope is None:
            return None, None

        # x domain...
        x_data = self.__x_data()

        min_x = min(x_data)
        max_x = max(x_data)

        mid_x = min_x + (max_x - min_x) / 2

        rec = LocalizedDatetime.construct_from_timestamp(mid_x)         # warning: uses current timezone

        # y val...
        val = slope * mid_x + intercept

        return rec, val


    # ----------------------------------------------------------------------------------------------------------------

    def __x_data(self):
        return [float(x) for x, _ in self.__data]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LinearRegression:{data:%s}" % self.__data
