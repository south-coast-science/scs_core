"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Recommended Minimum data
$xxRMC,datetime,status,lat,NS,long,EW,spd,cog,date,mv,mv_ew,pos_mode*cs

example:
$GPRMC,083559.00,A,4717.11437,N,00833.91522,E,0.004,77.52,091202,,,A*57
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
        # TODO cast to float / int as appropriate

        if s.field(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        time = s.field(1)
        status = s.field(2)

        lat = s.field(3)
        ns = s.field(4)

        lng = s.field(5)
        ew = s.field(6)

        loc = GPLoc(lat, ns, lng, ew)

        spd = s.field(7)
        cog = s.field(8)
        date = s.field(9)
        mv = s.field(10)
        mv_ew = s.field(11)

        pos_mode = s.field(12)

        datetime = GPDateTime(date, time)

        return GPRMC(datetime, status, loc, spd, cog, mv, mv_ew, pos_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, datetime, status, loc, spd, cog, mv, mv_ew, pos_mode):
        """
        Constructor
        """
        self.__datetime = datetime

        self.__status = status
        self.__loc = loc

        self.__spd = spd
        self.__cog = cog
        self.__mv = mv
        self.__mv_ew = mv_ew

        self.__pos_mode = pos_mode


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
