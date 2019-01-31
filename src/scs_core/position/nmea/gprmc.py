"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Recommended Minimum data
$xxRMC,datetime,status,lat,NS,long,EW,spd,cog,date,mv,mv_ew,pos_mode*cs

example sentence:
$GPRMC,083559.00,A,4717.11437,N,00833.91522,E,0.004,77.52,091202,,,A*57
$GNRMC,103953.00,A,5049.38023,N,00007.38608,W,0.195,,310119,,,D*72

example values:
GPRMC:{datetime:GPDateTime:{date:110117, time:141101.00}, status:A,
        loc:GPLoc:{lat:5049.38464, ns:N, lng:00007.37785, ew:W}, spd:0.005, cog:None, mv:None, mv_ew:None, pos_mode:D}

GPRMC:{datetime:GPDateTime:{date:110117, time:140047.00}, status:V,
        loc:GPLoc:{lat:None, ns:None, lng:None, ew:None}, spd:None, cog:None, mv:None, mv_ew:None, pos_mode:N}

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""

from scs_core.position.nmea.gpdatetime import GPDateTime
from scs_core.position.nmea.gploc import GPLoc
from scs_core.position.nmea.nmea_sentence import NMEASentence


# --------------------------------------------------------------------------------------------------------------------

class GPRMC(NMEASentence):
    """
    classdocs
    """

    MESSAGE_IDS = ("$GNRMC", "$GPRMC")

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, r):
        if r.message_id not in cls.MESSAGE_IDS:
            raise TypeError("invalid sentence:%s" % r)

        time = r.str(1)
        status = r.str(2)

        lat = r.str(3)
        ns = r.str(4)

        lng = r.str(5)
        ew = r.str(6)

        loc = GPLoc(lat, ns, lng, ew)

        spd = r.float(7, 3)
        cog = r.float(8, 2)
        date = r.str(9)
        mv = r.float(10, 2)
        mv_ew = r.str(11)

        pos_mode = r.str(12)

        datetime = GPDateTime(date, time)

        return GPRMC(r.message_id, datetime, status, loc, spd, cog, mv, mv_ew, pos_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, message_id, datetime, status, loc, spd, cog, mv, mv_ew, pos_mode):
        """
        Constructor
        """
        super().__init__(message_id)

        self.__datetime = datetime          # GPDateTime

        self.__status = status              # string
        self.__loc = loc                    # GPLoc

        self.__spd = spd                    # float(3) - speed over ground (knots)
        self.__cog = cog                    # float(2) - degrees course over ground
        self.__mv = mv                      # float(2) - degrees magnetic variation
        self.__mv_ew = mv_ew                # string - magnetic variation indicator

        self.__pos_mode = pos_mode          # string


    # ----------------------------------------------------------------------------------------------------------------

    def has_position(self):
        return self.__loc is not None and self.__loc.has_position()


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
        return "GPRMC:{source:%s, datetime:%s, status:%s, loc:%s, spd:%s, cog:%s, mv:%s, mv_ew:%s, pos_mode:%s}" % \
                    (self.source, self.datetime, self.status, self.loc, self.spd, self.cog, self.mv, self.mv_ew,
                     self.pos_mode)
