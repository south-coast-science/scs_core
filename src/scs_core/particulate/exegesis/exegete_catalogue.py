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

class ExegeteCatalogue(object):
    """
    classdocs
    """

    __MODELS = {
        # ISECEE...
        ISECEEN2v1.name(): ISECEEN2v1,
        ISECEER1v1.name(): ISECEER1v1,

        # ISECSE...
        ISECSEN2v1.name(): ISECSEN2v1,
        ISECSEN2v2.name(): ISECSEN2v2,
        ISECSEN3v1.name(): ISECSEN3v1,
        ISECSEN3v2.name(): ISECSEN3v2,

        # ISELUT...
        ISELUTN2v1.name(): ISELUTN2v1,
        ISELUTN3v1.name(): ISELUTN3v1
    }


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def model_names(cls):
        return sorted(cls.__MODELS.keys())


    @classmethod
    def load(cls, name, host):
        model = cls.__MODELS[name]

        return model.load(host)


    @classmethod
    def standard(cls, name):
        model = cls.__MODELS[name]

        return model.standard()
