"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: ISO country codes

NB: initialisation is performed at the foot of this class

example:
{"numeric": 788, "name": "Tunisia", "iso": "TUN"}

https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
https://www.airnow.gov/
"""

from scs_core.aqcsv.specification.country import Country


# --------------------------------------------------------------------------------------------------------------------

class CountryISO(Country):
    """
    classdocs
    """

    _retrieved = {}

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, numeric, name, iso):
        """
        Constructor
        """
        super().__init__(numeric, name, iso)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pk(self):
        return self.iso


# --------------------------------------------------------------------------------------------------------------------
# initialisation...

CountryISO.retrieve()
