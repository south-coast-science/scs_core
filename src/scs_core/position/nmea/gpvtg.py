"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Course over ground and Ground speed
$xxVTG,cogt,T,cogm,M,knots,N,kph,K,pos_mode*cs

example sentence:
$GPVTG,77.52,T,,M,0.004,N,0.008,K,A*06

example values:
GPVTG:{cogt:None, cogm:None, knots:0.005, kph:0.010, pos_mode:D}
GPVTG:{cogt:None, cogm:None, knots:None, kph:None, pos_mode:N}

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""


# --------------------------------------------------------------------------------------------------------------------

class GPVTG(object):
    """
    classdocs
    """

    MESSAGE_ID = "$GPVTG"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, s):
        if s.str(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        cogt = s.float(1, 2)
        cogm = s.float(3, 2)

        knots = s.float(5, 3)
        kph = s.float(7, 3)

        pos_mode = s.str(9)

        return GPVTG(cogt, cogm, knots, kph, pos_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cogt, cogm, knots, kph, pos_mode):
        """
        Constructor
        """
        self.__cogt = cogt                      # float(2) - degrees course over ground
        self.__cogm = cogm                      # float(2) - degrees course over ground (magnetic)

        self.__knots = knots                    # float(3) - speed over ground (knots)
        self.__kph = kph                        # float(3) - speed over ground (kph)

        self.__pos_mode = pos_mode              # string


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cogt(self):
        return self.__cogt


    @property
    def cogm(self):
        return self.__cogm


    @property
    def knots(self):
        return self.__knots


    @property
    def kph(self):
        return self.__kph


    @property
    def pos_mode(self):
        return self.__pos_mode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPVTG:{cogt:%s, cogm:%s, knots:%s, kph:%s, pos_mode:%s}" % \
                    (self.cogt, self.cogm, self.knots, self.kph, self.pos_mode)
