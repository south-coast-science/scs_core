'''
Created on 30 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Latitude and longitude, with time of position fix and status
$xxGLL,lat,NS,long,EW,time,status,posMode*cs

example:
$GPGLL,5049.37823,N,00007.37872,W,103228.00,A,D*7F
'''

from scs_core.location.gploc import GPLoc
from scs_core.location.gptime import GPTime


# --------------------------------------------------------------------------------------------------------------------

class GPGLL(object):
    '''
    classdocs
    '''

    MESSAGE_ID = "$GPGLL"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, s):
        if s.field(0) != cls.MESSAGE_ID:
            raise TypeError("invalid sentence:%s" % s)

        lat = s.field(1)
        ns = s.field(2)

        lng = s.field(3)
        ew = s.field(4)

        loc = GPLoc(lat, ns, lng, ew)

        time = GPTime(s.field(5))

        status = s.field(6)
        pos_mode = s.field(7)

        return GPGLL(loc, time, status, pos_mode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, loc, time, status, pos_mode):
        '''
        Constructor
        '''
        self.__loc = loc
        self.__time = time

        self.__status = status
        self.__pos_mode = pos_mode


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def loc(self):
        return self.__loc


    @property
    def time(self):
        return self.__time


    @property
    def status(self):
        return self.__status


    @property
    def pos_mode(self):
        return self.__pos_mode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPGLL:{loc:%s, time:%s, status:%s, pos_mode:%s}" % \
                    (self.loc, self.time, self.status, self.pos_mode)
