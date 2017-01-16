"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Course over ground and Ground speed
$xxVTG,cogt,T,cogm,M,knots,N,kph,K,pos_mode*cs

example:
$GPVTG,77.52,T,,M,0.004,N,0.008,K,A*06
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
        # TODO cast to float / int as appropriate

        if s.field(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        cogt = s.field(1)
        cogm = s.field(3)
        knots = s.field(5)
        kph = s.field(7)

        pos_mode = s.field(9)

        return GPVTG(cogt, cogm, knots, kph, pos_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cogt, cogm, knots, kph, pos_mode):
        """
        Constructor
        """
        self.__cogt = cogt
        self.__cogm = cogm
        self.__knots = knots
        self.__kph = kph

        self.__pos_mode = pos_mode


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
