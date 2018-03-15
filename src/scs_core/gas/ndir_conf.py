"""
Created on 15 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A stub class for an NDIRConf that may be implemented elsewhere
"""

from abc import abstractmethod

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRConf(PersistentJSONable):
    """
    classdocs
    """

    @classmethod
    def filename(cls, host):
        return None


    # ----------------------------------------------------------------------------------------------------------------
    # abstract NDIRConf...

    @abstractmethod
    def ndir_monitor(self, host):
        pass


    @property
    @abstractmethod
    def model(self):
        pass


    @property
    @abstractmethod
    def tally(self):
        pass
