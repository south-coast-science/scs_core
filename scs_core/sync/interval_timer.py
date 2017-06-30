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
            self.__sleep_until_next_yield()

            yield i


    def true(self):
        self.__sleep_until_next_yield()

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def __sleep_until_next_yield(self):
        sleep_time = (self.__next_yield - time.time()) % self.__interval        # this prevents negative intervals!

        if sleep_time > 0:
            try:
                time.sleep(sleep_time)
            except KeyboardInterrupt:
                pass

        self.__next_yield += self.__interval


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interval(self):
        return self.__interval


    @property
    def time_to_next_yield(self):
        return self.__next_yield - time.time()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IntervalTimer:{interval:%s, time_to_next_yield:%0.3f}" % (self.interval, self.time_to_next_yield)
