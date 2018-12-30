"""
Created on 10 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict
from numbers import Number

from scs_core.data.json import JSONable


# TODO: rename as GPSDatum?

# --------------------------------------------------------------------------------------------------------------------

class GPSLocation(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        lat = jdict.get('lat')
        lng = jdict.get('lng')
        alt = jdict.get('alt')

        quality = jdict.get('qual')

        return GPSLocation(lat, lng, alt, quality)


    @classmethod
    def construct(cls, gga):
        if gga is None:
            return None

        loc = gga.loc
        alt = None if gga.alt is None else round(gga.alt)
        quality = gga.quality

        if loc is None:
            return GPSLocation(None, None, alt, quality)

        lat = loc.deg_lat()
        lng = loc.deg_lng()

        return GPSLocation(lat, lng, alt, quality)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lat, lng, alt, quality):
        """
        Constructor
        """
        self.__lat = lat                    # degrees north of equator
        self.__lng = lng                    # degrees east of Greenwich meridian
        self.__alt = alt                    # metres above mean sea level

        self.__quality = quality            # 0 to 6 (?)


    # ----------------------------------------------------------------------------------------------------------------
    # Support for averaging...

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(other)

        lat = None if self.lat is None or other.lat is None else self.lat + other.lat
        lng = None if self.lng is None or other.lng is None else self.lng + other.lng
        alt = None if self.alt is None or other.alt is None else self.alt + other.alt

        quality = None if self.quality is None or other.quality is None else self.quality + other.quality

        return GPSLocation(lat, lng, alt, quality)


    def __truediv__(self, other):
        if not isinstance(other, Number):
            raise TypeError(other)

        lat = None if self.lat is None else self.lat / other
        lng = None if self.lng is None else self.lng / other
        alt = None if self.alt is None else self.alt / other

        quality = None if self.quality is None else self.quality / other

        return GPSLocation(lat, lng, alt, quality)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['lat'] = None if self.lat is None else round(self.lat, 7)
        jdict['lng'] = None if self.lng is None else round(self.lng, 7)
        jdict['alt'] = None if self.alt is None else round(self.alt, 1)

        jdict['qual'] = None if self.quality is None else int(round(self.quality))

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lat(self):
        return self.__lat


    @property
    def lng(self):
        return self.__lng


    @property
    def alt(self):
        return self.__alt


    @property
    def quality(self):
        return self.__quality


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSLocation:{lat:%s, lng:%s, alt:%s, quality:%s}" % (self.lat, self.lng, self.alt, self.quality)
