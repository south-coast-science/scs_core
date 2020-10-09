"""
Created on 31 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

GNSS Satellites in View
$xxGSV,numMsg,msgNum,numSV,{,sv,elv,az,cno}*cs

example sentence:
$GPGSV,3,1,10,  23,38,230,44,  29,71,156,47,  07,29,116,41,  08,09,081,36  *7F

example values:
GPGSV:{num_msg:3, msg_num:1, num_sv:12, sats:[GPSAT:{sv:02, elv:09, az:214, cno:28},
GPSAT:{sv:05, elv:70, az:230, cno:39}, GPSAT:{sv:07, elv:38, az:057, cno:None},
GPSAT:{sv:08, elv:00, az:060, cno:None}]}

GPGSV:{num_msg:1, msg_num:1, num_sv:01, sats:[GPSAT:{sv:02, elv:None, az:None, cno:26}]}

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""

from scs_core.data.str import Str
from scs_core.position.nmea.nmea_sentence import NMEASentence


# --------------------------------------------------------------------------------------------------------------------

class GPGSV(NMEASentence):
    """
    classdocs
    """

    MESSAGE_IDS = ("$GPGSV", )

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, r):
        if r.message_id not in cls.MESSAGE_IDS:
            raise TypeError("invalid sentence:%s" % r)

        num_msg = r.str(1)

        msg_num = r.str(2)
        num_sv = r.str(3)

        sats = [GPSAT(r.int(i), r.int(i + 1), r.int(i + 2), r.int(i + 3)) for i in range(4, len(r), 4)]

        return GPGSV(r.message_id, num_msg, msg_num, num_sv, sats)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, message_id, num_msg, msg_num, num_sv, sats):
        """
        Constructor
        """
        super().__init__(message_id)

        self.__num_msg = num_msg            # int
        self.__msg_num = msg_num            # int
        self.__num_sv = num_sv              # int

        self.__sats = sats                  # list of GPGSV


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def num_msg(self):
        return self.__num_msg


    @property
    def msg_num(self):
        return self.__msg_num


    @property
    def num_sv(self):
        return self.__num_sv


    @property
    def sats(self):
        return self.__sats


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPGSV:{source:%s, num_msg:%s, msg_num:%s, num_sv:%s, sats:%s}" % \
               (self.source, self.num_msg, self.msg_num, self.num_sv, Str.collection(self.__sats))


# --------------------------------------------------------------------------------------------------------------------

class GPSAT(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sv, elv, az, cno):
        """
        Constructor
        """
        self.__sv = sv              # int

        self.__elv = elv            # int
        self.__az = az              # int

        self.__cno = cno            # int


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sv(self):
        return self.__sv


    @property
    def elv(self):
        return self.__elv


    @property
    def az(self):
        return self.__az


    @property
    def cno(self):
        return self.__cno


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSAT:{sv:%s, elv:%s, az:%s, cno:%s}" % (self.sv, self.elv, self.az, self.cno)
