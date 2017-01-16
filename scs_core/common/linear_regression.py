'''
Created on 14 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from scs_core.common.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class LinearRegression(object):
    '''
    classdocs
    '''

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        '''
        Constructor
        '''
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

        min_x = min(x_data)
        max_x = max(x_data)

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
        sumX = 0
        sumY = 0

        sumXX = 0
        sumXY = 0

        # sum....
        for x, y in self.__data:
            sumX += x
            sumY += y

            sumXX += x * x
            sumXY += x * y

        # compute...
        avgX = sumX / n
        avgY = sumY / n

        dX = (sumXX * n) - (sumX * sumX)
        dY = (sumXY * n) - (sumX * sumY)

        slope = dY / dX
        intercept = avgY - (slope * avgX)

        return slope, intercept


    def __x_data(self):
        return [x for x, _ in self.__data]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "LinearRegression:{data:%s}" % self.__data
