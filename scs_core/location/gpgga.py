"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Global positioning system fix data
$xxGGA,time,lat,NS,long,EW,quality,numSV,HDOP,alt,M,sep,M,diffAge,diffStation*cs

example sentence:
$GPGGA,092725.00,4717.11399,N,00833.91590,E,1,08,1.01,499.6,M,48.0,M,,*5B

example values:
GPGGA:{time:GPTime:{time:141058.00}, loc:GPLoc:{lat:5049.38432, ns:N, lng:00007.37801, ew:W}, quality:2, num_sv:06, hdop:3.10, alt:37.5, sep:45.4, diff_age:None, diff_station:0000}
GPGGA:{time:GPTime:{time:140047.00}, loc:GPLoc:{lat:None, ns:None, lng:None, ew:None}, quality:0, num_sv:00, hdop:99.99, alt:None, sep:None, diff_age:None, diff_station:None}
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
        if s.str(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        time = GPTime(s.str(1))

        lat = s.str(2)
        ns = s.str(3)

        lng = s.str(4)
        ew = s.str(5)

        loc = GPLoc(lat, ns, lng, ew)

        quality = s.int(6)
        num_sv = s.int(7)
        hdop = s.float(8, 3)
        alt = s.float(9, 2)
        sep = s.float(11, 2)

        diff_age = s.float(13, 3)
        diff_station = s.str(14)

        return GPGGA(time, loc, quality, num_sv, hdop, alt, sep, diff_age, diff_station)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, time, loc, quality, num_sv, hdop, alt, sep, diff_age, diff_station):
        """
        Constructor
        """
        self.__time = time                          # GPTime
        self.__loc = loc                            # GPLoc

        self.__quality = quality                    # int
        self.__num_sv = num_sv                      # int
        self.__hdop = hdop                          # float(2)
        self.__alt = alt                            # float(1) - altitude (metres)
        self.__sep = sep                            # float(1) - geoid separation (metres)

        self.__diff_age = diff_age                  # float(3) - age of differential corrections (seconds)
        self.__diff_station = diff_station          # string - ID of station providing differential corrections


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
