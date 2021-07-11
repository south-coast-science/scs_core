"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: ISO country codes

example:
{"numeric": 788, "name": "Tunisia", "iso": "TUN"}

https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
https://www.airnow.gov/
"""

import os

from abc import ABC
from collections import OrderedDict

from scs_core.csv.csv_archive import CSVArchive
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Country(CSVArchive, JSONable, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        numeric = jdict.get('numeric')
        name = jdict.get('name')
        iso = jdict.get('iso')

        return cls(numeric, name, iso)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def archive_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive', 'countries.csv')


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, numeric, name, iso):
        """
        Constructor
        """
        self.__numeric = int(numeric)               # int(3)
        self.__name = name                          # string
        self.__iso = iso                            # string


    def __eq__(self, other):
        try:
            return self.numeric == other.numeric and self.name == other.name and self.iso == other.iso
        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['numeric'] = self.numeric
        jdict['name'] = self.name
        jdict['iso'] = self.iso

        return jdict


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
        return "Country:{numeric:%03d, name:%s, iso:%s}" % (self.numeric, self.name, self.iso)
