"""
Created on 15 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A stub class for an NDIRConf that may be implemented elsewhere
"""

from abc import abstractmethod
from collections import OrderedDict

from scs_core.data.json import PersistentJSONable
from scs_core.gas.ndir_monitor import NDIRMonitor


# --------------------------------------------------------------------------------------------------------------------

class NDIRConf(PersistentJSONable):
    """
    classdocs
    """

    _FILENAME = "ndir_conf.json"

    @classmethod
    def filename(cls, host):
        return None             # prevent instances of this class from constructing real NDIRs


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


    # ----------------------------------------------------------------------------------------------------------------

    def ndir_monitor(self, host):
        return NDIRMonitor(self.ndir(host), self)


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
