"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import re

from collections import OrderedDict

from scs_core.aqcsv.specification.country import Country
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class AQCSVSite(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_code(cls, code):
        if not code:
            return None
        try:
            match = re.match('(\d{3})(MM)?(\d{9})', code)
        except TypeError:
            raise ValueError(code)

        if match is None:
            raise ValueError(code)

        fields = match.groups()

        country_code = fields[0]
        location_code = fields[2]
        is_mobile = fields[1] is not None

        return AQCSVSite(country_code, location_code, is_mobile)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, country_code, location_code, is_mobile):
        """
        Constructor
        """
        self.__country_code = country_code                  # string
        self.__location_code = location_code                # string
        self.__is_mobile = is_mobile                        # bool


    # ----------------------------------------------------------------------------------------------------------------

    def as_code(self):
        mobility_code = 'MM' if self.is_mobile else ''

        return self.country_code + mobility_code + self.location_code


    def as_json(self):
        jdict = OrderedDict()

        jdict['country-code'] = self.country_code
        jdict['location-code'] = self.location_code
        jdict['is-mobile'] = self.is_mobile

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def country(self):
        return Country.find_by_numeric(self.country_code)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def country_code(self):
        return self.__country_code


    @property
    def location_code(self):
        return self.__location_code


    @property
    def is_mobile(self):
        return self.__is_mobile


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AQCSVSite:{country_code:%s, location_code:%s, is_mobile:%s}" % \
               (self.country_code, self.location_code, self.is_mobile)
