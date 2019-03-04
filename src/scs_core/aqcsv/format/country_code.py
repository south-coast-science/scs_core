"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"numeric": 788, "name": "Tunisia", "iso": "TUN"}

https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
"""

import json
import os

from collections import OrderedDict

from scs_core.csv.csv_reader import CSVReader
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class CountryCode(JSONable):
    """
    classdocs
    """

    __codes = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls):
        directory = os.path.dirname(os.path.realpath(__file__))
        filename = directory + "/codes/country_codes.csv"

        reader = CSVReader(filename)

        try:
            for row in reader.rows:
                code = cls.construct_from_jdict(json.loads(row))
                cls.__codes[code.iso] = code

        finally:
            reader.close()

    @classmethod
    def codes(cls):
        for code in cls.__codes.values():
            yield code


    @classmethod
    def find_by_iso(cls, iso):
        if iso not in cls.__codes:
            return None

        return cls.__codes[iso]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        numeric = jdict.get('numeric')
        name = jdict.get('name')
        iso = jdict.get('iso')


        return CountryCode(numeric, name, iso)


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
        return "CountryCode:{numeric:%s, name:%s, iso:%s}" %  (self.numeric, self.name, self.iso)
