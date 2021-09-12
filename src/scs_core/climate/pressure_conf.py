"""
Created on 9 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"model": "ICP", "altitude": 100}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class PressureConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "pressure_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return cls(None, None) if skeleton else None

        model = jdict.get('model')
        altitude = jdict.get('altitude')

        return cls(model, altitude)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, altitude):
        """
        Constructor
        """
        super().__init__()

        self.__model = model                    # string
        self.__altitude = altitude              # int, 'GPS' or None


    def __eq__(self, other):
        try:
            return self.model == other.model or self.altitude == other.altitude

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def altitude(self):
        return self.__altitude


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.__model
        jdict['altitude'] = self.__altitude

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PressureConf(core):{model:%s, altitude:%s}" % (self.model, self.altitude)
