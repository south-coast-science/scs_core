"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
"location": {
    "lat": 50.819456,
    "lon": -0.128336,
    "postcode": "bn2 1af"
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Location(JSONable):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        lat = jdict.get('lat')
        lng = jdict.get('lon')

        elevation = jdict.get('elevation')

        zipcode = jdict.get('zip')
        postcode = jdict.get('postcode')

        return Location(lat, lng, elevation, zipcode, postcode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lat, lng, elevation, zipcode, postcode):
        """
        Constructor
        """
        self.__lat = lat                    # float
        self.__lng = lng                    # float

        self.__elevation = elevation        # int

        self.__zip = zipcode                # string
        self.__postcode = postcode          # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['lat'] = self.lat
        jdict['lon'] = self.lng

        if self.elevation is not None:
            jdict['elevation'] = self.elevation

        if self.zip:
            jdict['zip'] = self.zip

        jdict['postcode'] = self.postcode

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def lat(self):
        return self.__lat


    @property
    def lng(self):
        return self.__lng


    @property
    def elevation(self):
        return self.__elevation


    @property
    def zip(self):
        return self.__zip


    @property
    def postcode(self):
        return None if self.__postcode is None else self.__postcode.upper()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Location:{lat:%s, lng:%s, elevation:%s, zip:%s, postcode:%s}" % \
                        (self.lat, self.lng, self.elevation, self.zip, self.postcode)
