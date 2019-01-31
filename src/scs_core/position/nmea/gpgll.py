"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Latitude and longitude, with time of position fix and status
$xxGLL,lat,NS,long,EW,time,status,posMode*cs

example sentence:
$GPGLL,5049.37823,N,00007.37872,W,103228.00,A,D*7F

example values:
GPGLL:{loc:GPLoc:{lat:5049.38432, ns:N, lng:00007.37801, ew:W}, time:GPTime:{time:141058.00}, status:A, pos_mode:D}
GPGLL:{loc:GPLoc:{lat:None, ns:None, lng:None, ew:None}, time:GPTime:{time:140047.00}, status:V, pos_mode:N}

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""

from scs_core.position.nmea.gploc import GPLoc
from scs_core.position.nmea.gptime import GPTime
from scs_core.position.nmea.nmea_sentence import NMEASentence


# --------------------------------------------------------------------------------------------------------------------

class GPGLL(NMEASentence):
    """
    classdocs
    """

    MESSAGE_IDS = ("$GNGLL", "$GPGLL")

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, r):
        if r.message_id not in cls.MESSAGE_IDS:
            raise TypeError("invalid sentence:%s" % r)

        lat = r.str(1)
        ns = r.str(2)

        lng = r.str(3)
        ew = r.str(4)

        loc = GPLoc(lat, ns, lng, ew)

        time = GPTime(r.str(5))

        status = r.str(6)
        pos_mode = r.str(7)

        return GPGLL(r.message_id, loc, time, status, pos_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, message_id, loc, time, status, pos_mode):
        """
        Constructor
        """
        super().__init__(message_id)

        self.__loc = loc                    # GPLoc
        self.__time = time                  # GPTime

        self.__status = status              # string
        self.__pos_mode = pos_mode          # string


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def loc(self):
        return self.__loc


    @property
    def time(self):
        return self.__time


    @property
    def status(self):
        return self.__status


    @property
    def pos_mode(self):
        return self.__pos_mode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPGLL:{source:%s, loc:%s, time:%s, status:%s, pos_mode:%s}" % \
               (self.source, self.loc, self.time, self.status, self.pos_mode)
