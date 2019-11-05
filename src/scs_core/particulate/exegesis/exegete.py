"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a catalogue of particulate exegesis models
"""

from scs_core.particulate.exegesis.isecee_n2_v001 import ISECEEN2v1
from scs_core.particulate.exegesis.isecse_n2_v001 import ISECSEN2v1


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
        return [ISECEEN2v1.name(), ISECSEN2v1.name()]


    @staticmethod
    def load(name, host):
        if name == ISECEEN2v1.name():
            return ISECEEN2v1.load(host)

        if name == ISECSEN2v1.name():
            return ISECSEN2v1.load(host)

        raise ValueError(name)


    @staticmethod
    def standard(name):
        if name == ISECEEN2v1.name():
            return ISECEEN2v1.standard()

        if name == ISECSEN2v1.name():
            return ISECSEN2v1.standard()

        raise ValueError(name)
