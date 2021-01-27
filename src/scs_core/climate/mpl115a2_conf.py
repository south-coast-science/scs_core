"""
Created on 21 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies fixed altitude or "auto" (altitude provided by GPS receiver), or None

example JSON:
{"altitude": "auto"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class MPL115A2Conf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "mpl115a2_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        altitude = jdict.get('altitude')

        return MPL115A2Conf(altitude)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, altitude):
        """
        Constructor
        """
        self.__altitude = altitude              # int, "auto" or None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def altitude(self):
        return self.__altitude


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['altitude'] = self.__altitude

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MPL115A2Conf:{altitude:%s}" % self.altitude
