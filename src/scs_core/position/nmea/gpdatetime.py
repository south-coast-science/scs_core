"""
Created on 1 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""


# --------------------------------------------------------------------------------------------------------------------

class GPDateTime(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, date, time):
        """
        Constructor
        """
        self.__date = date                # ddmmyy
        self.__time = time                # hhmmss.ss


    # ----------------------------------------------------------------------------------------------------------------

    def as_iso8601(self):
        """
        example: 2016-08-13T00:38:05.210+00:00
        """
        if self.__date is None or self.__time is None:
            return None

        return "20%s-%s-%sT%s:%s:%s0Z" % \
               (self.__date[4:], self.__date[2:4], self.__date[:2], self.__time[:2], self.__time[2:4], self.__time[4:])


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def date(self):
        return self.__date


    @property
    def time(self):
        return self.__time


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPDateTime:{date:%s, time:%s}" % (self.date, self.time)
