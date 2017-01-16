"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

GNSS DOP and Active Satellites
$xxGSA,opMode,navMode{,sv},PDOP,HDOP,VDOP*cs

example:
$GPGSA,A,3,23,29,07,08,09,18,26,28,,,,,1.94,1.18,1.54*0D
"""


# --------------------------------------------------------------------------------------------------------------------

class GPGSA(object):
    """
    classdocs
    """

    MESSAGE_ID = "$GPGSA"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, s):
        # TODO cast to float / int as appropriate

        if s.field(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        op_mode = s.field(1)
        nav_mode = s.field(2)

        sv = []
        for i in range(12):
            sv.append(s.field(3 + i))

        pdop = s.field(15)
        hdop = s.field(16)
        vdop = s.field(17)

        return GPGSA(op_mode, nav_mode, sv, pdop, hdop, vdop)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, op_mode, nav_mode, sv, pdop, hdop, vdop):
        """
        Constructor
        """
        self.__op_mode = op_mode
        self.__nav_mode = nav_mode
        
        self.__sv = sv

        self.__pdop = pdop
        self.__hdop = hdop
        self.__vdop = vdop


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def op_mode(self):
        return self.__op_mode


    @property
    def nav_mode(self):
        return self.__nav_mode


    @property
    def sv(self):
        return self.__sv


    @property
    def pdop(self):
        return self.__pdop


    @property
    def hdop(self):
        return self.__hdop


    @property
    def vdop(self):
        return self.__vdop


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        svs = '[' + ', '.join([str(sv) for sv in self.__sv]) + ']'

        return "GPGSA:{op_mode:%s, nav_mode:%s, sv:%s, pdop:%s, hdop:%s, vdop:%s}" % \
                    (self.op_mode, self.nav_mode, svs, self.pdop, self.hdop, self.vdop)
