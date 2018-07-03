"""
Created on 10 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example use:
./socket_receiver.py | ./csv_writer.py status.csv -e | ./histo_chart.py val.loc.lat -v -e -o lat.csv -x 50.8228 50.8232
./socket_receiver.py | ./csv_writer.py status.csv -e | ./histo_chart.py val.loc.lng -v -e -o lng.csv -x -0.1233 -0.1227
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


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
        self.__lat = lat                    # degrees north of the equator
        self.__lng = lng                    # degrees east of Greenwich
        self.__alt = alt                    # metres above sea level

        self.__quality = quality            # 0 to 3


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['lat'] = self.lat
        jdict['lng'] = self.lng
        jdict['alt'] = self.alt

        jdict['qual'] = self.quality

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
