"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a catalogue of particulate exegesis models
"""

from scs_core.particulate.exegesis.isecen2_v001 import ISECEN2v1


# --------------------------------------------------------------------------------------------------------------------

class Exegete(object):
    """
    classdocs
    """

    __ROOT = 'exg'

    @classmethod
    def root(cls):
        return cls.__ROOT


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def models():
        return [ISECEN2v1.name()]


    @staticmethod
    def model(name, host):
        if name == ISECEN2v1.name():
            return ISECEN2v1.load(host)

        raise ValueError(name)
