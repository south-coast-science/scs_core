'''
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

GNSS DOP and Active Satellites
$xxGSA,opMode,navMode{,sv},PDOP,HDOP,VDOP*cs

example sentence:
$GPGSA,A,3,23,29,07,08,09,18,26,28,,,,,1.94,1.18,1.54*0D

example values:
GPGSA:{op_mode:A, nav_mode:3, sv:[21, 02, 28, 13, 30, 05, None, None, None, None, None, None], pdop:4.61, hdop:3.10, vdop:3.41}
GPGSA:{op_mode:A, nav_mode:1, sv:[None, None, None, None, None, None, None, None, None, None, None, None], pdop:99.99, hdop:99.99, vdop:99.99}
'''


# --------------------------------------------------------------------------------------------------------------------

class GPGSA(object):
    '''
    classdocs
    '''

    MESSAGE_ID = "$GPGSA"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, s):
        if s.str(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        op_mode = s.str(1)
        nav_mode = s.int(2)

        sv = []
        for i in range(12):
            sv.append(s.int(3 + i))

        pdop = s.float(15, 2)
        hdop = s.float(16, 2)
        vdop = s.float(17, 2)

        return GPGSA(op_mode, nav_mode, sv, pdop, hdop, vdop)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, op_mode, nav_mode, sv, pdop, hdop, vdop):
        '''
        Constructor
        '''
        self.__op_mode = op_mode            # string
        self.__nav_mode = nav_mode          # int
        
        self.__sv = sv                      # list of int

        self.__pdop = pdop                  # float(2)
        self.__hdop = hdop                  # float(2)
        self.__vdop = vdop                  # float(2)


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
        svs = '[' + ', '.join(str(sv) for sv in self.__sv) + ']'

        return "GPGSA:{op_mode:%s, nav_mode:%s, sv:%s, pdop:%s, hdop:%s, vdop:%s}" % \
                    (self.op_mode, self.nav_mode, svs, self.pdop, self.hdop, self.vdop)
