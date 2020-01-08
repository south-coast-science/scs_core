"""
Created on 17 Dec 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Stacey Beloff Logothetis, Type 1

An error model in which each rH delta is associated with a specific temperature response curve; successive rH delta
response curves form a surface, where the x and y axes represent the independent variables T and rH, and the z axis
represents the predicted error.

In both T and rH dimensions, response curves are assumed to be continuous, and are found using numpy polyfit.

Meteo data should be gained from the Praxis "external" SHT31 sensor. In Type 1, no account is taken of the T or rH
hysteresis of either the electrochem or the SHT31.

https://docs.scipy.org/doc/numpy/reference/generated/numpy.polyfit.html
https://joshualoong.com/2018/10/03/Fitting-Polynomial-Regressions-in-Python/
"""

from abc import ABC
from collections import OrderedDict

from scs_core.error.error_surface import ErrorSurface
from scs_core.gas.exegesis.exegete import Exegete


# --------------------------------------------------------------------------------------------------------------------

class SBL1(Exegete, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return cls.standard()

        surfaces = OrderedDict()

        for gas in jdict.keys():
            surfaces[gas] = ErrorSurface.construct_from_jdict(jdict[gas])

        return cls(surfaces)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), "gas_exegete_" + cls.name() + "_calib.json"


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, surfaces):
        """
        Constructor
        """
        super().__init__()

        self.__surfaces = surfaces                              # dict of gas: ErrorSurface


    def __eq__(self, other):
        try:
            for gas in self.gases():
                if self.__surfaces[gas] != other.__surfaces[gas]:
                    return False

        except KeyError:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def gases(self):
        return list(self.__surfaces.keys())


    def interpretation(self, gas, text, t, rh):
        return text - self.error(gas, t, rh)


    def error(self, gas, t, rh):
        surface = self.__surfaces[gas]                          # may raise KeyError

        return surface.error(t, rh)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__surfaces


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        surfaces = '{' + ', '.join(gas + ': ' + str(surface) for gas, surface in self.__surfaces.items()) + '}'

        return self.__class__.__name__ + ":{surfaces:%s}" % surfaces
