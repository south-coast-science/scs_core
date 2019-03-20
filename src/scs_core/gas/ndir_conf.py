"""
Created on 15 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A stub class for an NDIRConf that may be implemented elsewhere
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRConf(ABC, PersistentJSONable):
    """
    classdocs
    """

    _FILENAME = "ndir_conf.json"

    @classmethod
    def persistence_location(cls, host):
        raise NotImplementedError()


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model, tally):
        """
        Constructor
        """
        super().__init__()

        self.__model = model
        self.__tally = tally


    # ----------------------------------------------------------------------------------------------------------------
    # abstract NDIRConf...

    @abstractmethod
    def ndir(self, host):
        pass


    @abstractmethod
    def ndir_monitor(self, host):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.model
        jdict['tally'] = self.tally

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    @property
    def tally(self):
        return self.__tally


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRConf:{model:%s, tally:%s}" %  (self.model, self.tally)
