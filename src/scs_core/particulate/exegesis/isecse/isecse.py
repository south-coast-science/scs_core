"""
Created on 11 Nov 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

method: Immediate Scaling Error / Curve is Single Exponential (ISECSE)

domain: 0 <= rH <= max_rh
model: error = ce * e ^ (cx * rH)
range: PM / error
"""

from abc import ABC
from collections import OrderedDict
from math import exp

from scs_core.data.datum import Format

from scs_core.particulate.exegesis.exegete import Exegete
from scs_core.particulate.exegesis.text import Text


# --------------------------------------------------------------------------------------------------------------------

class ISECSE(Exegete, ABC):
    """
    classdocs
    """

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


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ce, cx, max_rh_pm1, max_rh_pm2p5, max_rh_pm10):
        """
        Constructor
        """
        super().__init__()

        self.__ce = ce                                      # coefficient of e              dict of float
        self.__cx = cx                                      # coefficient of x              dict of float

        self.__max_rh_pm1 = int(max_rh_pm1)                 # maximum rH for PM1            int
        self.__max_rh_pm2p5 = int(max_rh_pm2p5)             # maximum rH for PM2.5          int
        self.__max_rh_pm10 = int(max_rh_pm10)               # maximum rH for PM10           int


    def __eq__(self, other):
        return self.__ce == other.__ce and \
               self.__cx == other.__cx and \
               self.__max_rh_pm1 == other.__max_rh_pm1 and \
               self.__max_rh_pm2p5 == other.__max_rh_pm2p5 and \
               self.__max_rh_pm10 == other.__max_rh_pm10


    # ----------------------------------------------------------------------------------------------------------------

    def interpretation(self, datum, rh):
        pm1 = self.__interpretation('pm1', datum.pm1, rh, self.__max_rh_pm1)
        pm2p5 = self.__interpretation('pm2p5', datum.pm2p5, rh, self.__max_rh_pm2p5)
        pm10 = self.__interpretation('pm10', datum.pm10, rh, self.__max_rh_pm10)

        return Text(pm1, pm2p5, pm10)


    def error(self, species, rh):
        ce = self.__ce[species]
        cx = self.__cx[species]

        return ce * exp(cx * rh)


    # ----------------------------------------------------------------------------------------------------------------

    def __interpretation(self, species, pm, rh, max_rh):
        if pm is None or rh is None:
            return None

        if rh > max_rh:
            return None

        return pm / self.error(species, rh)


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
        ce = Format.collection(self.__ce)
        cx = Format.collection(self.__cx)

        return self.__class__.__name__ + ":{ce:%s, cx:%s, max_rh_pm1:%s, max_rh_pm2p5:%s, max_rh_pm10:%s}" % \
            (ce, cx, self.__max_rh_pm1, self.__max_rh_pm2p5, self.__max_rh_pm10)
