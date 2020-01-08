"""
Created on 8 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a catalogue of gas exegesis models, as required by configuration tools
"""

from scs_core.gas.exegesis.sbl1.sbl1_v1 import SBL1v1


# --------------------------------------------------------------------------------------------------------------------

class ExegeteCatalogue(object):
    """
    classdocs
    """

    __MODELS = {
        # SBL1...
        SBL1v1.name(): SBL1v1
    }


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def model_names(cls):
        return sorted(cls.__MODELS.keys())


    @classmethod
    def load(cls, name, host):
        model = cls.__MODELS[name]                                  # may raise KeyError

        return model.load(host)


    @classmethod
    def standard(cls, name):
        model = cls.__MODELS[name]                                  # may raise KeyError

        return model.standard()
