"""
Created on 11 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time


# TODO: deal with the case where network time is not available yet

# --------------------------------------------------------------------------------------------------------------------

class IntervalTimer(object):
    """
    generate indices at pre-set intervals
    """

    def __init__(self, interval):
        self.__interval = interval
        self.__next_yield = time.time() + self.__interval


    # ----------------------------------------------------------------------------------------------------------------

    def range(self, stop):
        for i in range(stop):
            sleep_time = self.__next_yield - time.time()

            if sleep_time > 0:
                time.sleep(sleep_time)

            self.__next_yield += self.__interval

            yield i


    def true(self):
        sleep_time = self.__next_yield - time.time()

        if sleep_time > 0:
            time.sleep(sleep_time)

        self.__next_yield += self.__interval

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interval(self):
        return self.__interval


    @property
    def time_to_next_yield(self):
        return self.__next_yield - time.time()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IntervalTimer:{interval:%d, time_to_next_yield:%0.3f}" % (self.interval, self.time_to_next_yield)
