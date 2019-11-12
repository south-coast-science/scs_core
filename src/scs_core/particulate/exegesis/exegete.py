"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a catalogue of particulate exegesis models
"""

from scs_core.particulate.exegesis.isecee.isecee_n2_v001 import ISECEEN2v1
from scs_core.particulate.exegesis.isecee.isecee_r1_v001 import ISECEER1v1

from scs_core.particulate.exegesis.isecse.isecse_n2_v001 import ISECSEN2v1
from scs_core.particulate.exegesis.isecse.isecse_n2_v002 import ISECSEN2v2


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
        return [ISECEEN2v1.name(), ISECEER1v1.name(), ISECSEN2v1.name(), ISECSEN2v2.name()]


    @staticmethod
    def load(name, host):
        # ISECEE...
        if name == ISECEEN2v1.name():
            return ISECEEN2v1.load(host)

        if name == ISECEER1v1.name():
            return ISECEER1v1.load(host)

        # ISECSE...
        if name == ISECSEN2v1.name():
            return ISECSEN2v1.load(host)

        if name == ISECSEN2v2.name():
            return ISECSEN2v2.load(host)

        raise ValueError(name)


    @staticmethod
    def standard(name):
        # ISECEE...
        if name == ISECEEN2v1.name():
            return ISECEEN2v1.standard()

        if name == ISECEER1v1.name():
            return ISECEER1v1.standard()

        # ISECSE...
        if name == ISECSEN2v1.name():
            return ISECSEN2v1.standard()

        if name == ISECSEN2v2.name():
            return ISECSEN2v2.standard()

        raise ValueError(name)
