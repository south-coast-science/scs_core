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

from scs_core.position.nmea.nmea_sentence import NMEASentence


# --------------------------------------------------------------------------------------------------------------------

class GPVTG(NMEASentence):
    """
    classdocs
    """

    MESSAGE_IDS = ("$GNVTG", "$GPVTG")

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, r):
        if r.message_id not in cls.MESSAGE_IDS:
            raise TypeError("invalid sentence:%s" % r)

        cogt = r.float(1, 2)
        cogm = r.float(3, 2)

        knots = r.float(5, 3)
        kph = r.float(7, 3)

        pos_mode = r.str(9)

        return GPVTG(r.message_id, cogt, cogm, knots, kph, pos_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, message_id, cogt, cogm, knots, kph, pos_mode):
        """
        Constructor
        """
        super().__init__(message_id)

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
        return "GPVTG:{source:%s, cogt:%s, cogm:%s, knots:%s, kph:%s, pos_mode:%s}" % \
                    (self.source, self.cogt, self.cogm, self.knots, self.kph, self.pos_mode)
