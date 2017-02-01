"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Recommended Minimum data
$xxRMC,datetime,status,lat,NS,long,EW,spd,cog,date,mv,mv_ew,pos_mode*cs

example sentence:
$GPRMC,083559.00,A,4717.11437,N,00833.91522,E,0.004,77.52,091202,,,A*57

example values:
GPRMC:{datetime:GPDateTime:{date:110117, time:141101.00}, status:A, loc:GPLoc:{lat:5049.38464, ns:N, lng:00007.37785, ew:W}, spd:0.005, cog:None, mv:None, mv_ew:None, pos_mode:D}
GPRMC:{datetime:GPDateTime:{date:110117, time:140047.00}, status:V, loc:GPLoc:{lat:None, ns:None, lng:None, ew:None}, spd:None, cog:None, mv:None, mv_ew:None, pos_mode:N}
"""

from scs_core.location.gpdatetime import GPDateTime
from scs_core.location.gploc import GPLoc


# --------------------------------------------------------------------------------------------------------------------

class GPRMC(object):
    """
    classdocs
    """

    MESSAGE_ID = "$GPRMC"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, s):
        if s.str(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        time = s.str(1)
        status = s.str(2)

        lat = s.str(3)
        ns = s.str(4)

        lng = s.str(5)
        ew = s.str(6)

        loc = GPLoc(lat, ns, lng, ew)

        spd = s.float(7, 3)
        cog = s.float(8, 2)
        date = s.str(9)
        mv = s.float(10, 2)
        mv_ew = s.str(11)

        pos_mode = s.str(12)

        datetime = GPDateTime(date, time)

        return GPRMC(datetime, status, loc, spd, cog, mv, mv_ew, pos_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, datetime, status, loc, spd, cog, mv, mv_ew, pos_mode):
        """
        Constructor
        """
        self.__datetime = datetime          # GPDateTime

        self.__status = status              # string
        self.__loc = loc                    # GPLoc

        self.__spd = spd                    # float(3) - speed over ground (knots)
        self.__cog = cog                    # float(2) - degrees course over ground
        self.__mv = mv                      # float(2) - degrees magnetic variation
        self.__mv_ew = mv_ew                # string - magnetic variation indicator

        self.__pos_mode = pos_mode          # string


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def datetime(self):
        return self.__datetime


    @property
    def status(self):
        return self.__status


    @property
    def loc(self):
        return self.__loc


    @property
    def spd(self):
        return self.__spd


    @property
    def cog(self):
        return self.__cog


    @property
    def mv(self):
        return self.__mv


    @property
    def mv_ew(self):
        return self.__mv_ew


    @property
    def pos_mode(self):
        return self.__pos_mode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPRMC:{datetime:%s, status:%s, loc:%s, spd:%s, cog:%s, mv:%s, mv_ew:%s, pos_mode:%s}" % \
                    (self.datetime, self.status, self.loc, self.spd, self.cog, self.mv, self.mv_ew, self.pos_mode)
