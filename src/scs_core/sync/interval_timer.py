"""
Created on 11 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time


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
            try:
                self.__sleep_until_next_yield()
            except KeyboardInterrupt:
                return stop

            yield i


    def true(self):
        try:
            self.__sleep_until_next_yield()
        except KeyboardInterrupt:
            return False

        return True


    def reset(self):
        self.__next_yield = time.time() + self.__interval


    # ----------------------------------------------------------------------------------------------------------------

    def __sleep_until_next_yield(self):
        if self.__interval == 0:
            return

        sleep_time = (self.__next_yield - time.time()) % self.__interval        # prevents negative intervals

        if sleep_time == 0:
            sleep_time = self.__interval        # prevents zero intervals

        time.sleep(sleep_time)

        self.__next_yield += self.__interval


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interval(self):
        return self.__interval


    @property
    def time_to_next_yield(self):
        return abs(self.__next_yield - time.time())         # time to next must always be positive


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IntervalTimer:{interval:%s, time_to_next_yield:%s}" % \
               (round(self.interval, 1), round(self.time_to_next_yield, 1))
