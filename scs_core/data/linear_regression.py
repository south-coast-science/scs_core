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

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__data = []


    def __len__(self):
        return len(self.__data)


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, rec: LocalizedDatetime, val):
        self.__data.append((rec.timestamp(), val))


    def midpoint(self):
        slope, intercept = self.__line()

        # validate...
        if slope is None:
            return None, None

        # x domain...
        x_data = self.__x_data()

        min_x = min(x_data)[0]
        max_x = max(x_data)[0]

        mid_x = min_x + (max_x - min_x) / 2

        rec = LocalizedDatetime.construct_from_timestamp(mid_x)         # warning: uses current timezone

        # y val...
        val = slope * mid_x + intercept

        return rec, val


    def reset(self):
        self.__data = []


    # ----------------------------------------------------------------------------------------------------------------

    def __line(self):
        n = len(self)

        # validate...
        if n < 3:
            return None, None

        # init...
        sum_x = 0
        sum_y = 0

        sum_xx = 0
        sum_xy = 0

        # sum....
        for x, y in self.__data:
            sum_x += x
            sum_y += y

            sum_xx += x * x
            sum_xy += x * y

        # compute...
        avg_x = sum_x / n
        avg_y = sum_y / n

        d_x = (sum_xx * n) - (sum_x * sum_x)
        d_y = (sum_xy * n) - (sum_x * sum_y)

        slope = d_y / d_x
        intercept = avg_y - (slope * avg_x)

        return slope, intercept


    def __x_data(self):
        return [x for x, _ in self.__data]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LinearRegression:{data:%s}" % self.__data
