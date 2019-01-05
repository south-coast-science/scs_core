"""
Created on 10 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""

from collections import OrderedDict
from numbers import Number

from scs_core.data.json import JSONable
from scs_core.position.position import Position


# --------------------------------------------------------------------------------------------------------------------

class GPSDatum(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        if 'alt' in jdict:
            pos = Position(jdict.get('lat'), jdict.get('lng'))
            elv = jdict.get('alt')

        else:
            pos = Position.construct_from_jdict(jdict.get('pos'))
            elv = jdict.get('elv')

        quality = jdict.get('qual')

        return GPSDatum(pos, elv, quality)


    @classmethod
    def construct_from_gga(cls, gga):
        if gga is None:
            return None

        pos = Position.construct_from_gga(gga)
        elv = None if gga.alt is None else round(gga.alt)

        quality = gga.quality

        return GPSDatum(pos, elv, quality)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, pos, elv, quality):
        """
        Constructor
        """
        self.__pos = pos                    # Position
        self.__elv = elv                    # metres above mean sea level

        self.__quality = quality            # 0 to 6 (?)


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

    def as_json(self):
        jdict = OrderedDict()

        jdict['pos'] = self.pos.as_json()
        jdict['elv'] = None if self.elv is None else round(self.elv, 1)

        jdict['qual'] = None if self.quality is None else int(round(self.quality))

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


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSDatum:{pos:%s, elv:%s, quality:%s}" % (self.pos, self.elv, self.quality)
