"""
Created on 15 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A stub class for an NDIRConf that may be implemented elsewhere
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "ndir_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        model = jdict.get('model')
        tally = jdict.get('tally')
        raw = jdict.get('raw', False)

        return cls(model, tally, raw)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, tally, raw=False):
        """
        Constructor
        """
        super().__init__()

        self.__model = model
        self.__tally = tally
        self.__raw = raw


    def __eq__(self, other):
        try:
            return self.model == other.model and self.tally == other.tally and self.raw == other.raw

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def ndir_monitor(self, interface, host):
        return None


    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def ndir(self, interface, host):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.model
        jdict['tally'] = self.tally
        jdict['raw'] = self.raw

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def tally(self):
        return self.__tally


    @property
    def raw(self):
        return self.__raw


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRConf(core):{model:%s, tally:%s, raw:%s}" %  (self.model, self.tally, self.raw)
