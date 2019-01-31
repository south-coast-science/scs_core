"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Global positioning system fix data
$xxGGA,time,lat,NS,long,EW,quality,numSV,HDOP,alt,M,sep,M,diffAge,diffStation*cs

example sentence:
$GPGGA,092725.00,4717.11399,N,00833.91590,E,1,08,1.01,499.6,M,48.0,M,,*5B

example values:
GPGGA:{time:GPTime:{time:141058.00}, loc:GPLoc:{lat:5049.38432, ns:N, lng:00007.37801, ew:W}, quality:2, num_sv:06,
hdop:3.10, alt:37.5, sep:45.4, diff_age:None, diff_station:0000}

GPGGA:{time:GPTime:{time:140047.00}, loc:GPLoc:{lat:None, ns:None, lng:None, ew:None}, quality:0, num_sv:00,
hdop:99.99, alt:None, sep:None, diff_age:None, diff_station:None}

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""

from scs_core.position.nmea.gploc import GPLoc
from scs_core.position.nmea.gptime import GPTime
from scs_core.position.nmea.nmea_sentence import NMEASentence


# --------------------------------------------------------------------------------------------------------------------

class GPGGA(NMEASentence):
    """
    classdocs
    """

    MESSAGE_IDS = ("$GNGGA", "$GPGGA")

    QUALITY_NO_FIX =                0
    QUALITY_AUTONOMOUS_GNSS =       1
    QUALITY_DIFFERENTIAL_GNSS =     2
    QUALITY_ESTIMATED_FIX =         6


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, r):
        if r.message_id not in cls.MESSAGE_IDS:
            raise TypeError("invalid sentence:%s" % r)

        time = GPTime(r.str(1))

        lat = r.str(2)
        ns = r.str(3)

        lng = r.str(4)
        ew = r.str(5)

        loc = GPLoc(lat, ns, lng, ew)

        quality = r.int(6)
        num_sv = r.int(7)
        hdop = r.float(8, 3)
        alt = r.float(9, 2)
        sep = r.float(11, 2)

        diff_age = r.float(13, 3)
        diff_station = r.str(14)

        return GPGGA(r.message_id, time, loc, quality, num_sv, hdop, alt, sep, diff_age, diff_station)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, message_id, time, loc, quality, num_sv, hdop, alt, sep, diff_age, diff_station):
        """
        Constructor
        """
        super().__init__(message_id)

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
        return "GPGGA:{source:%s, time:%s, loc:%s, quality:%s, num_sv:%s, hdop:%s, alt:%s, sep:%s, " \
               "diff_age:%s, diff_station:%s}" % \
                    (self.source, self.time, self.loc, self.quality, self.num_sv, self.hdop, self.alt, self.sep,
                     self.diff_age, self.diff_station)
