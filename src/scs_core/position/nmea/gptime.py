"""
Created on 1 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""


# --------------------------------------------------------------------------------------------------------------------

class GPTime(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, time):
        """
        Constructor
        """
        self.__time = time                # string - hhmmss.ss


    # ----------------------------------------------------------------------------------------------------------------

    def as_iso8601(self):
        """
        example: 00:38:05.210Z
        """
        if self.__time is None:
            return None

        return "%s:%s:%s0Z" % (self.__time[:2], self.__time[2:4], self.__time[4:])


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def time(self):
        return self.__time


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPTime:{time:%s}" % self.time
