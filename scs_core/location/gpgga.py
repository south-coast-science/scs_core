"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Global positioning system fix data
$xxGGA,time,lat,NS,long,EW,quality,numSV,HDOP,alt,M,sep,M,diffAge,diffStation*cs

example:
$GPGGA,092725.00,4717.11399,N,00833.91590,E,1,08,1.01,499.6,M,48.0,M,,*5B
"""

from scs_core.location.gploc import GPLoc
from scs_core.location.gptime import GPTime


# --------------------------------------------------------------------------------------------------------------------

class GPGGA(object):
    """
    classdocs
    """

    MESSAGE_ID = "$GPGGA"

    QUALITY_NO_FIX =                0
    QUALITY_AUTONOMOUS_GNSS =       1
    QUALITY_DIFFERENTIAL_GNSS =     2
    QUALITY_ESTIMATED_FIX =         6


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, s):
        # TODO cast to float / int as appropriate

        if s.field(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        time = GPTime(s.field(1))

        lat = s.field(2)
        ns = s.field(3)

        lng = s.field(4)
        ew = s.field(5)

        loc = GPLoc(lat, ns, lng, ew)

        quality = s.field(6)
        num_sv = s.field(7)
        hdop = s.field(8)
        alt = s.field(9)
        sep = s.field(11)

        diff_age = s.field(13)
        diff_station = s.field(14)

        return GPGGA(time, loc, quality, num_sv, hdop, alt, sep, diff_age, diff_station)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, time, loc, quality, num_sv, hdop, alt, sep, diff_age, diff_station):
        """
        Constructor
        """
        self.__time = time
        self.__loc = loc

        self.__quality = quality
        self.__num_sv = num_sv
        self.__hdop = hdop
        self.__alt = alt
        self.__sep = sep

        self.__diff_age = diff_age
        self.__diff_station = diff_station


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def time(self):
        return self.__time


    @property
    def loc(self):
        return self.__loc


    @property
    def quality(self):
        return self.__quality


    @property
    def num_sv(self):
        return self.__num_sv


    @property
    def hdop(self):
        return self.__hdop


    @property
    def alt(self):
        return self.__alt


    @property
    def sep(self):
        return self.__sep


    @property
    def diff_age(self):
        return self.__diff_age


    @property
    def diff_station(self):
        return self.__diff_station


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPGGA:{time:%s, loc:%s, quality:%s, num_sv:%s, hdop:%s, alt:%s, sep:%s, diff_age:%s, diff_station:%s}" % \
                    (self.time, self.loc, self.quality, self.num_sv, self.hdop, self.alt, self.sep, self.diff_age, self.diff_station)
