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
    def construct(cls, gga):
        if gga is None:
            return None

        quality = gga.quality

        loc = gga.loc

        if loc is None:
            return GPSLocation(None, None, quality)

        lat = loc.deg_lat()
        lng = loc.deg_lng()

        return GPSLocation(lat, lng, quality)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lat, lng, quality):
        """
        Constructor
        """
        self.__lat = lat
        self.__lng = lng
        self.__quality = quality


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['lat'] = self.lat
        jdict['lng'] = self.lng
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
    def quality(self):
        return self.__quality


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GPSLocation:{lat:%s, lng:%s, quality:%s}" % (self.lat, self.lng, self.quality)
