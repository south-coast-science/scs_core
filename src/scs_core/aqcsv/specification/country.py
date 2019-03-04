"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: ISO country codes

example:
{"numeric": "716", "name": "Zimbabwe", "iso": "ZWE"}

https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_archived import CSVArchived
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Country(JSONable, CSVArchived):
    """
    classdocs
    """

    _retrieved = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def archive_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive', 'countries.csv')


    @classmethod
    def find_by_numeric(cls, numeric):
        for country in cls._retrieved.values():
            if country.numeric == numeric:
                return country

        return None


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        numeric = jdict.get('numeric')
        name = jdict.get('name')
        iso = jdict.get('iso')

        return Country(numeric, name, iso)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, numeric, name, iso):
        """
        Constructor
        """
        self.__numeric = numeric                    # string
        self.__name = name                          # string
        self.__iso = iso                            # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['numeric'] = self.numeric
        jdict['name'] = self.name
        jdict['iso'] = self.iso

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pk(self):
        return self.iso


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def numeric(self):
        return self.__numeric


    @property
    def name(self):
        return self.__name


    @property
    def iso(self):
        return self.__iso


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Country:{numeric:%s, name:%s, iso:%s}" % (self.numeric, self.name, self.iso)
