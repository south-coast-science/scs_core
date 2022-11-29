"""
Created on 10 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183

reference coordinate systems:
https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
https://en.wikipedia.org/wiki/PZ-90
"""

from collections import OrderedDict
from numbers import Number

from scs_core.data.datum import Datum
from scs_core.data.json import JSONReport

from scs_core.position.position import Position


# --------------------------------------------------------------------------------------------------------------------

class GPSDatum(JSONReport):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls.null_datum()

        pos = Position.construct_from_jdict(jdict.get('pos'))
        elv = jdict.get('elv')

        quality = jdict.get('qual')

        return cls(pos, elv, quality)


    @classmethod
    def construct_from_gga(cls, gga):
        if gga is None:
            return None

        pos = Position.construct_from_gga(gga)
        elv = None if gga.alt is None else round(gga.alt)

        quality = gga.quality

        return cls(pos, elv, quality)


    @classmethod
    def null_datum(cls):
        return cls(Position(None, None), None, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pos, elv, quality):
        """
        Constructor
        """
        self.__pos = pos                            # Position
        self.__elv = Datum.float(elv, 1)            # metres above mean sea level

        self.__quality = quality                    # number or None


    # ----------------------------------------------------------------------------------------------------------------
    # Support for averaging...

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(other)

        pos = self.pos + other.pos
        elv = self.elv + other.elv

        quality = self.quality + other.quality

        return GPSDatum(pos, elv, quality)


    def __truediv__(self, other):
        if not isinstance(other, Number):
            raise TypeError(other)

        pos = self.pos / other
        elv = self.elv / other

        quality = self.quality / other

        return GPSDatum(pos, elv, quality)


    # ----------------------------------------------------------------------------------------------------------------

    def distance(self, other_pos, minimum_acceptable_quality=None):
        if self.pos is None:
            return None

        if minimum_acceptable_quality is not None:
            if self.quality is None or round(self.quality) < minimum_acceptable_quality:
                return None

        return self.pos.distance(other_pos)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['pos'] = self.pos
        jdict['elv'] = None if self.elv is None else round(self.elv, 1)

        jdict['qual'] = None if self.quality is None else round(self.quality, 1)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pos(self):
        return self.__pos


    @property
    def elv(self):
        return self.__elv


    @property
    def quality(self):
        return self.__quality


    @quality.setter
    def quality(self, quality):
        self.__quality = quality


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSDatum:{pos:%s, elv:%s, quality:%s}" % (self.pos, self.elv, self.quality)
