"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a catalogue of particulate exegesis models
"""

from scs_core.particulate.exegesis.isecee.isecee_n2_v001 import ISECEEN2v1
from scs_core.particulate.exegesis.isecee.isecee_r1_v001 import ISECEER1v1

from scs_core.particulate.exegesis.isecse.isecse_n2_v001 import ISECSEN2v1
from scs_core.particulate.exegesis.isecse.isecse_n2_v002 import ISECSEN2v2
from scs_core.particulate.exegesis.isecse.isecse_n3_v001 import ISECSEN3v1
from scs_core.particulate.exegesis.isecse.isecse_n3_v002 import ISECSEN3v2

from scs_core.particulate.exegesis.iselut.iselut_n2_v001 import ISELUTN2v1
from scs_core.particulate.exegesis.iselut.iselut_n3_v001 import ISELUTN3v1


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
        return [
            ISECEEN2v1.name(),
            ISECEER1v1.name(),
            ISECSEN2v1.name(),
            ISECSEN2v2.name(),
            ISECSEN3v1.name(),
            ISECSEN3v2.name(),
            ISELUTN2v1.name(),
            ISELUTN3v1.name()
        ]


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

        if name == ISECSEN3v1.name():
            return ISECSEN3v1.load(host)

        if name == ISECSEN3v2.name():
            return ISECSEN3v2.load(host)

        # ISELUT...
        if name == ISELUTN2v1.name():
            return ISELUTN2v1.load(host)

        if name == ISELUTN3v1.name():
            return ISELUTN3v1.load(host)

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

        if name == ISECSEN3v1.name():
            return ISECSEN3v1.standard()

        if name == ISECSEN3v2.name():
            return ISECSEN3v2.standard()

        # ISELUT...
        if name == ISELUTN2v1.name():
            return ISELUTN2v1.standard()

        if name == ISELUTN3v1.name():
            return ISELUTN3v1.standard()

        raise ValueError(name)
