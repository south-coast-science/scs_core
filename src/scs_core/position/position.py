"""
Created on 5 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://en.wikipedia.org/wiki/Geographic_coordinate_system
"""

from numbers import Number

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Position(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        lat = jdict[0]
        lng = jdict[1]

        return Position(lat, lng)


    @classmethod
    def construct_from_gga(cls, gga):
        if gga is None:
            return None

        loc = gga.loc

        lat = None if loc is None else loc.deg_lat()
        lng = None if loc is None else loc.deg_lng()

        return Position(lat, lng)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lat, lng):
        """
        Constructor
        """
        self.__lat = lat                    # float     degrees north of equator (±90)
        self.__lng = lng                    # float     degrees east of Greenwich meridian (±180)


    # ----------------------------------------------------------------------------------------------------------------
    # Support for averaging...

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(other)

        lat = self.lat + other.lat
        lng = self.lng + other.lng

        return Position(lat, lng)


    def __truediv__(self, other):
        if not isinstance(other, Number):
            raise TypeError(other)

        lat = self.lat / other
        lng = self.lng / other

        return Position(lat, lng)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jlist = (
            None if self.lat is None else round(self.lat, 8),
            None if self.lng is None else round(self.lng, 8)
        )

        return jlist


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lat(self):
        return self.__lat


    @property
    def lng(self):
        return self.__lng


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Position:{lat:%s, lng:%s}" % (self.lat, self.lng)
