"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
  {
    "client-id": "5891",
    "description": "BB development platform",
    "name": "Praxis/BGB 000000",
    "tags": [
      "pm1",
      "pm2.5",
      "pm10",
      "co",
      "no",
      "no2",
      "o3",
      "temperature",
      "humidity"
    ],
    "location": {
      "lat": 50.82313,
      "lon": -0.122922,
      "postcode": "bn2 0da"
    }
  },
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.osio.data.location import Location


# --------------------------------------------------------------------------------------------------------------------

class DeviceSummary(JSONable):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        client_id = jdict.get('client-id')
        name = jdict.get('name')
        description = jdict.get('description')

        location = Location.construct_from_jdict(jdict.get('location'))

        tags = jdict.get('tags')

        device = DeviceSummary(client_id, name, description, location, tags)

        return device


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client_id, name, description, location, tags):
        """
        Constructor
        """
        self.__client_id = client_id                        # string (int by convention)
        self.__name = name                                  # string
        self.__description = description                    # string

        self.__location = location                          # Location

        self.__tags = tags                                  # array of string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.client_id is not None:
            jdict['client-id'] = self.client_id

        jdict['name'] = self.name
        jdict['description'] = self.description

        if self.location is not None:
            jdict['location'] = self.location

        jdict['tags'] = self.tags

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def client_id(self):
        return self.__client_id


    @property
    def name(self):
        return self.__name


    @property
    def description(self):
        return self.__description


    @property
    def location(self):
        return self.__location


    @property
    def tags(self):
        return self.__tags


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceSummary:{client_id:%s, name:%s, description:%s, location:%s, tags:%s}" % \
                    (self.client_id, self.name, self.description, self.location, self.tags)
