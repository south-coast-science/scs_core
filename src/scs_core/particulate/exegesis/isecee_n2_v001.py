"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

THIS CODE SHALL BE TREATED AS IMMUTABLE. THUS, ANY ALTERATIONS TO EQUATIONS OR STANDARD COEFFICIENTS SHALL BE
PRESENTED AS A NEW CLASS, WITH AN INCREMENTED CLASS VERSION NUMBER.

Coefficients gained from Alphasense OPC-N2 (versus Palas Fidas) data at LHR2 in 2019.

method: Immediate Scaling Error / Curve is Elbow Exponential (ISECEE), OPC-N2, version 1

domain: 0 <= rH <= max_rh
model: error = ceLOW * e ^ (cxLOW * rH) where rH < elbow
model: error = ceHIGH * e ^ (cxHIGH * rH) where rH => elbow
range: PM / error
"""

from collections import OrderedDict
from math import exp

from scs_core.data.json import PersistentJSONable
from scs_core.particulate.exegesis.text import Text


# --------------------------------------------------------------------------------------------------------------------

class ISECEEN2v1(PersistentJSONable):
    """
    classdocs
    """

    __NAME =                            "iseceen2v1"

    __STANDARD_CE_LOW = OrderedDict()
    __STANDARD_CE_LOW['pm1'] =          0.6029
    __STANDARD_CE_LOW['pm2p5'] =        0.6208
    __STANDARD_CE_LOW['pm10'] =         0.5375

    __STANDARD_CX_LOW = OrderedDict()
    __STANDARD_CX_LOW['pm1'] =          0.0195
    __STANDARD_CX_LOW['pm2p5'] =        0.0208
    __STANDARD_CX_LOW['pm10'] =         0.0213

    __STANDARD_CE_HIGH = OrderedDict()
    __STANDARD_CE_HIGH['pm1'] =         0.1605
    __STANDARD_CE_HIGH['pm2p5'] =       0.1924
    __STANDARD_CE_HIGH['pm10'] =        0.0177

    __STANDARD_CX_HIGH = OrderedDict()
    __STANDARD_CX_HIGH['pm1'] =         0.0398
    __STANDARD_CX_HIGH['pm2p5'] =       0.0389
    __STANDARD_CX_HIGH['pm10'] =        0.0728

    __STANDARD_CE = OrderedDict()
    __STANDARD_CE['low'] = __STANDARD_CE_LOW
    __STANDARD_CE['high'] = __STANDARD_CE_HIGH

    __STANDARD_CX = OrderedDict()
    __STANDARD_CX['low'] = __STANDARD_CX_LOW
    __STANDARD_CX['high'] = __STANDARD_CX_HIGH

    __STANDARD_rH_ELBOW =               61                      # percent relative humidity

    __STANDARD_MAX_rH_PM1 =             100
    __STANDARD_MAX_rH_PM2p5 =           100
    __STANDARD_MAX_rH_PM10 =            85

    @classmethod
    def name(cls):
        return cls.__NAME


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "particulate_exegete_" + __NAME + "_calib.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return cls.standard()

        ce = jdict.get('ce')
        cx = jdict.get('cx')

        rh_elbow = jdict.get('rh-elbow')

        max_rh_pm1 = jdict.get('max-rh-pm1')
        max_rh_pm2p5 = jdict.get('max-rh-pm2p5')
        max_rh_pm10 = jdict.get('max-rh-pm10')

        return cls(ce, cx, rh_elbow, max_rh_pm1, max_rh_pm2p5, max_rh_pm10)


    @classmethod
    def standard(cls):
        return cls(cls.__STANDARD_CE, cls.__STANDARD_CX, cls.__STANDARD_rH_ELBOW,
                   cls.__STANDARD_MAX_rH_PM1, cls.__STANDARD_MAX_rH_PM2p5, cls.__STANDARD_MAX_rH_PM10)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ce, cx, rh_elbow, max_rh_pm1, max_rh_pm2p5, max_rh_pm10):
        """
        Constructor
        """
        super().__init__()

        self.__ce = ce                                      # coefficient of e          dict of dict of float
        self.__cx = cx                                      # coefficient of x          dict of dict of float

        self.__rh_elbow = int(rh_elbow)                     # lower to higher rH boundary       int

        self.__max_rh_pm1 = int(max_rh_pm1)                 # maximum rH for PM1                int
        self.__max_rh_pm2p5 = int(max_rh_pm2p5)             # maximum rH for PM2.5              int
        self.__max_rh_pm10 = int(max_rh_pm10)               # maximum rH for PM10               int


    def __eq__(self, other):
        return self.__ce == other.__ce and \
               self.__cx == other.__cx and \
               self.__max_rh_pm1 == other.__max_rh_pm1 and \
               self.__max_rh_pm2p5 == other.__max_rh_pm2p5 and \
               self.__max_rh_pm10 == other.__max_rh_pm10


    # ----------------------------------------------------------------------------------------------------------------

    def interpret(self, datum, rh):
        pm1 = self.__interpret('pm1', datum.pm1, rh, self.__max_rh_pm1)
        pm2p5 = self.__interpret('pm2p5', datum.pm2p5, rh, self.__max_rh_pm2p5)
        pm10 = self.__interpret('pm10', datum.pm10, rh, self.__max_rh_pm10)

        return Text(pm1, pm2p5, pm10)


    def tag(self):
        if self == self.standard():
            return self.__NAME

        return self.__NAME + '?'                            # indicates non-standard coefficients


    # ----------------------------------------------------------------------------------------------------------------

    def __interpret(self, species, pm, rh, max_rh):
        if pm is None or rh is None:
            return None

        if rh > max_rh:
            return None

        return pm / self.__error(species, rh)


    def __error(self, species, rh):
        zone = 'low' if rh < self.__rh_elbow else 'high'

        ce = self.__ce[zone][species]
        cx = self.__cx[zone][species]

        # print("species:%s rH:%s zone:%s ce:%s cx:%s" % (species, rh, zone, ce, cx))

        return ce * exp(cx * rh)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['ce'] = self.__ce
        jdict['cx'] = self.__cx

        jdict['rh-elbow'] = self.__rh_elbow

        jdict['max-rh-pm1'] = self.__max_rh_pm1
        jdict['max-rh-pm2p5'] = self.__max_rh_pm2p5
        jdict['max-rh-pm10'] = self.__max_rh_pm10

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ISECEEN2v1:{ce:%s, cx:%s, max_rh_pm1:%s, max_rh_pm2p5:%s, max_rh_pm10:%s}" % \
               (self.__ce, self.__cx, self.__max_rh_pm1, self.__max_rh_pm2p5, self.__max_rh_pm10)
