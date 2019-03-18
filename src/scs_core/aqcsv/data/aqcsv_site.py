"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.airnow.gov/
"""

import re

from scs_core.aqcsv.specification.country_numeric import CountryNumeric

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class AQCSVSite(JSONable):
    """
    classdocs
    """

    LOCATION_CODE_LENGTH = 9

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_code(cls, code):
        if code is None:
            return None
        try:
            match = re.match(r'(\d{3})(MM)?(\d{9}).*', str(code))
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
        self.__country_code = int(country_code)             # int(3)
        self.__location_code = location_code                # string
        self.__is_mobile = is_mobile                        # bool


    def __eq__(self, other):
        try:
            return \
                self.country_code == other.country_code and \
                self.location_code == other.location_code and \
                self.is_mobile == other.is_mobile

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.as_code()


    def as_code(self):
        mobility_code = 'MM' if self.is_mobile else ''

        return str(self.country_code) + str(mobility_code) + str(self.location_code)


    # ----------------------------------------------------------------------------------------------------------------

    def country(self):
        return CountryNumeric.instance(self.country_code)


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
        return "AQCSVSite:{country_code:%03d, location_code:%s, is_mobile:%s}" % \
               (self.country_code, self.location_code, self.is_mobile)
