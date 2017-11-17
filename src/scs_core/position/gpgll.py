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
"""

from scs_core.position.gploc import GPLoc
from scs_core.position.gptime import GPTime


# --------------------------------------------------------------------------------------------------------------------

class GPGLL(object):
    """
    classdocs
    """

    MESSAGE_ID = "$GPGLL"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, s):
        if s.str(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        lat = s.str(1)
        ns = s.str(2)

        lng = s.str(3)
        ew = s.str(4)

        loc = GPLoc(lat, ns, lng, ew)

        time = GPTime(s.str(5))

        status = s.str(6)
        pos_mode = s.str(7)

        return GPGLL(loc, time, status, pos_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, loc, time, status, pos_mode):
        """
        Constructor
        """
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
        return "GPGLL:{loc:%s, time:%s, status:%s, pos_mode:%s}" % \
                    (self.loc, self.time, self.status, self.pos_mode)
