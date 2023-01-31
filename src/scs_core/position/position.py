"""
Created on 5 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Getting distance between two points based on latitude/longitude
https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude

https://en.wikipedia.org/wiki/Geographic_coordinate_system
"""

from math import sin, cos, sqrt, atan2, radians
from numbers import Number

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Position(JSONable):
    """
    classdocs
    """

    R = 6373.0              # approximate radius of earth in Km

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        lat = jdict[0]
        lng = jdict[1]

        if lat == '':
            lat = None

        if lng == '':
            lng = None

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
        self.__lat = lat                    # float     degrees north of the equator (±90)
        self.__lng = lng                    # float     degrees east of the Greenwich meridian (±180)


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

    def distance(self, other):
        if other is None:
            return None

        if not isinstance(other, self.__class__):
            raise TypeError(other)

        if other.lat is None or other.lng is None:
            return None

        lat1 = radians(self.lat)
        lng1 = radians(self.lng)

        lat2 = radians(other.lat)
        lng2 = radians(other.lng)

        delta_lat = lat2 - lat1
        delta_lng = lng2 - lng1

        a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lng / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = self.R * c

        return round(distance, 3)


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
