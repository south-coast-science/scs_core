"""
Created on 10 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""

from collections import OrderedDict
from numbers import Number

from scs_core.data.json import JSONable


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

        lat = jdict.get('lat')
        lng = jdict.get('lng')
        alt = jdict.get('alt')

        quality = jdict.get('qual')

        return GPSDatum(lat, lng, alt, quality)


    @classmethod
    def construct(cls, gga):
        if gga is None:
            return None

        loc = gga.loc
        alt = None if gga.alt is None else round(gga.alt)
        quality = gga.quality

        if loc is None:
            return GPSDatum(None, None, alt, quality)

        lat = loc.deg_lat()
        lng = loc.deg_lng()

        return GPSDatum(lat, lng, alt, quality)


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

        lat = self.lat + other.lat
        lng = self.lng + other.lng
        alt = self.alt + other.alt

        quality = self.quality + other.quality

        return GPSDatum(lat, lng, alt, quality)


    def __truediv__(self, other):
        if not isinstance(other, Number):
            raise TypeError(other)

        lat = self.lat / other
        lng = self.lng / other
        alt = self.alt / other

        quality = self.quality / other

        return GPSDatum(lat, lng, alt, quality)


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
        return "GPSDatum:{lat:%s, lng:%s, alt:%s, quality:%s}" % (self.lat, self.lng, self.alt, self.quality)
