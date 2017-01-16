'''
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Location(JSONable):
    '''
    classdocs
   '''

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        lat = jdict.get('lat')
        lng = jdict.get('lon')

        elevation = jdict.get('elevation')

        zip = jdict.get('zip')
        postcode = jdict.get('postcode')

        return Location(lat, lng, elevation, zip, postcode)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lat, lng, elevation, zip, postcode):
        '''
        Constructor
        '''
        self.__lat = lat                    # float
        self.__lng = lng                    # float

        self.__elevation = elevation        # int

        self.__zip = zip                    # string
        self.__postcode = postcode          # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['lat'] = self.lat
        jdict['lon'] = self.lng

        jdict['elevation'] = self.elevation

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
        return self.__postcode


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Location:{lat:%s, lng:%s, elevation:%s, zip:%s, postcode:%s}" % \
                        (self.lat, self.lng, self.elevation, self.zip, self.postcode)
