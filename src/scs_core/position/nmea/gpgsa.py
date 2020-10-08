"""
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

GNSS DOP and Active Satellites
$xxGSA,opMode,navMode{,sv},PDOP,HDOP,VDOP*cs

example sentence:
$GPGSA,A,3,23,29,07,08,09,18,26,28,,,,,1.94,1.18,1.54*0D

example values:
GPGSA:{op_mode:A, nav_mode:3, sv:[21, 02, 28, 13, 30, 05, None, None, None, None, None, None], pdop:4.61,
hdop:3.10, vdop:3.41}

GPGSA:{op_mode:A, nav_mode:1, sv:[None, None, None, None, None, None, None, None, None, None, None, None], pdop:99.99,
hdop:99.99, vdop:99.99}

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""

from scs_core.data.str import Str
from scs_core.position.nmea.nmea_sentence import NMEASentence


# --------------------------------------------------------------------------------------------------------------------

class GPGSA(NMEASentence):
    """
    classdocs
    """

    MESSAGE_IDS = ("$GNGSA", "$GPGSA")

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, r):
        if r.message_id not in cls.MESSAGE_IDS:
            raise TypeError("invalid sentence:%s" % r)

        op_mode = r.str(1)
        nav_mode = r.int(2)

        sv = [r.int(i + 3) for i in range(12)]

        pdop = r.float(15, 2)
        hdop = r.float(16, 2)
        vdop = r.float(17, 2)

        return GPGSA(r.message_id, op_mode, nav_mode, sv, pdop, hdop, vdop)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, message_id, op_mode, nav_mode, sv, pdop, hdop, vdop):
        """
        Constructor
        """
        super().__init__(message_id)

        self.__op_mode = op_mode            # string
        self.__nav_mode = nav_mode          # int

        self.__sv = sv                      # list of int

        self.__pdop = pdop                  # float(2)
        self.__hdop = hdop                  # float(2)
        self.__vdop = vdop                  # float(2)


    def __eq__(self, other):
        try:
            return self.op_mode == other.op_mode and self.nav_mode == other.nav_mode and self.sv == other.sv and \
                   self.pdop == other.pdop and self.hdop == other.hdop and self.vdop == other.vdop

        except AttributeError:
            return False


    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return not self == other


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
        return "GPGSA:{source:%s, op_mode:%s, nav_mode:%s, sv:%s, pdop:%s, hdop:%s, vdop:%s}" % \
               (self.source, self.op_mode, self.nav_mode, Str.collection(self.__sv), self.pdop, self.hdop, self.vdop)
