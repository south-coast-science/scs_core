"""
Created on 31 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

GNSS Satellites in View
$xxGSV,numMsg,msgNum,numSV,{,sv,elv,az,cno}*cs

example:
$GPGSV,3,1,10,  23,38,230,44,  29,71,156,47,  07,29,116,41,  08,09,081,36  *7F
"""


# --------------------------------------------------------------------------------------------------------------------

class GPGSV(object):
    """
    classdocs
    """

    MESSAGE_ID = "$GPGSV"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, s):
        # TODO cast to float / int as appropriate

        if s.field(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        num_msg = s.field(1)

        msg_num = s.field(2)
        num_sv = s.field(3)

        sats = []
        for i in range(4, len(s), 4):
            sats.append(GPSAT(s.field(i), s.field(i + 1), s.field(i + 2), s.field(i + 3)))

        return GPGSV(num_msg, msg_num, num_sv, sats)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, num_msg, msg_num, num_sv, sats):
        """
        Constructor
        """
        self.__num_msg = num_msg
        self.__msg_num = msg_num
        self.__num_sv = num_sv

        self.__sats = sats


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
        sats = '[' + ', '.join([str(sat) for sat in self.__sats]) + ']'

        return "GPGSV:{num_msg:%s, msg_num:%s, num_sv:%s, sats:%s}" % \
                    (self.num_msg, self.msg_num, self.num_sv, sats)


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
        self.__sv = sv

        self.__elv = elv
        self.__az = az

        self.__cno = cno


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
        return "GPSAT:{sv:%s, elv:%s, az:%s, cno:%s}" % \
                    (self.sv, self.elv, self.az, self.cno)
