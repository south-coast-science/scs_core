"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

THIS CODE SHALL BE TREATED AS IMMUTABLE. THUS, ANY ALTERATIONS TO EQUATIONS OR STANDARD COEFFICIENTS SHALL BE
PRESENTED AS A NEW CLASS, WITH AN INCREMENTED CLASS VERSION NUMBER.

Coefficients gained from Alphasense OPC-N2 (versus Palas Fidas) data at LHR2 in 2019.

method: Immediate Scaling Error / Curve is Single Exponential (ISECSE), OPC-N2, version 1

domain: 0 <= rH <= max_rh
model: error = ce * e ^ (cx * rH)
range: PM / error
"""

from collections import OrderedDict
from math import exp

from scs_core.data.json import PersistentJSONable
from scs_core.particulate.exegesis.text import Text


# --------------------------------------------------------------------------------------------------------------------

class ISECSEN2v1(PersistentJSONable):
    """
    classdocs
    """

    __NAME =                        "isecsen2v1"

    __STANDARD_CE =                 0.44
    __STANDARD_CX =                 0.027

    __STANDARD_MAX_rH_PM1 =         100
    __STANDARD_MAX_rH_PM2p5 =       100
    __STANDARD_MAX_rH_PM10 =        85

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

        max_rh_pm1 = jdict.get('max-rh-pm1')
        max_rh_pm2p5 = jdict.get('max-rh-pm2p5')
        max_rh_pm10 = jdict.get('max-rh-pm10')

        return cls(ce, cx, max_rh_pm1, max_rh_pm2p5, max_rh_pm10)


    @classmethod
    def standard(cls):
        return cls(cls.__STANDARD_CE, cls.__STANDARD_CX,
                   cls.__STANDARD_MAX_rH_PM1, cls.__STANDARD_MAX_rH_PM2p5, cls.__STANDARD_MAX_rH_PM10)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ce, cx, max_rh_pm1, max_rh_pm2p5, max_rh_pm10):
        """
        Constructor
        """
        super().__init__()

        self.__ce = float(ce)                               # coefficient of e
        self.__cx = float(cx)                               # coefficient of x

        self.__max_rh_pm1 = int(max_rh_pm1)                 # maximum rH for PM1
        self.__max_rh_pm2p5 = int(max_rh_pm2p5)             # maximum rH for PM2.5
        self.__max_rh_pm10 = int(max_rh_pm10)               # maximum rH for PM10


    def __eq__(self, other):
        return self.__ce == other.__ce and \
               self.__cx == other.__cx and \
               self.__max_rh_pm1 == other.__max_rh_pm1 and \
               self.__max_rh_pm2p5 == other.__max_rh_pm2p5 and \
               self.__max_rh_pm10 == other.__max_rh_pm10


    # ----------------------------------------------------------------------------------------------------------------

    def interpret(self, datum, rh):
        pm1 = self.__interpret(datum.pm1, rh, self.__max_rh_pm1)
        pm2p5 = self.__interpret(datum.pm2p5, rh, self.__max_rh_pm2p5)
        pm10 = self.__interpret(datum.pm10, rh, self.__max_rh_pm10)

        return Text(pm1, pm2p5, pm10)


    def tag(self):
        if self == self.standard():
            return self.__NAME

        return self.__NAME + '?'                            # indicates non-standard coefficients


    # ----------------------------------------------------------------------------------------------------------------

    def __interpret(self, pm, rh, max_rh):
        if pm is None or rh is None:
            return None

        if rh > max_rh:
            return None

        return pm / self.__error(rh)


    def __error(self, rh):
        return self.__ce * exp(self.__cx * rh)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['ce'] = self.__ce
        jdict['cx'] = self.__cx

        jdict['max-rh-pm1'] = self.__max_rh_pm1
        jdict['max-rh-pm2p5'] = self.__max_rh_pm2p5
        jdict['max-rh-pm10'] = self.__max_rh_pm10

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ISECSEN2v1:{ce:%s, cx:%s, max_rh_pm1:%s, max_rh_pm2p5:%s, max_rh_pm10:%s}" % \
               (self.__ce, self.__cx, self.__max_rh_pm1, self.__max_rh_pm2p5, self.__max_rh_pm10)
