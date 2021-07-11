"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: Agency codes

NB: initialisation is performed at the foot of this class

example:
{"code": "LBL", "name": "Lawrence Berkeley National Laboratory"}

https://www.airnow.gov/
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_archive import CSVArchive

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Agency(CSVArchive, JSONable):
    """
    classdocs
    """

    _retrieved = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def archive_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive', 'agencies.csv')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        code = jdict.get('code')
        name = jdict.get('name')

        return Agency(code, name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, name):
        """
        Constructor
        """
        self.__code = code                                  # string
        self.__name = name                                  # string


    def __eq__(self, other):
        try:
            return self.code == other.code and self.name == other.name

        except AttributeError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['code'] = self.code
        jdict['name'] = self.name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pk(self):
        return self.code


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def name(self):
        return self.__name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Agency:{code:%s, name:%s}" % (self.code, self.name)


# --------------------------------------------------------------------------------------------------------------------
# initialisation...

Agency.retrieve()
