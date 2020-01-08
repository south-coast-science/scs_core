"""
Created on 9 Dec 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a collection of particulate exegesis models, required by sampling tools
"""

from collections import OrderedDict

from scs_core.particulate.exegesis.exegete_catalogue import ExegeteCatalogue


# --------------------------------------------------------------------------------------------------------------------

class ExegeteCollection(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, exegete_names):
        exegetes = []

        for exegete_name in exegete_names:
            exegetes.append(ExegeteCatalogue.standard(exegete_name))                # may raise KeyError

        return cls(exegetes)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, exegetes):
        """
        Constructor
        """
        self.__exegetes = exegetes


    def __len__(self):
        return len(self.__exegetes)


    # ----------------------------------------------------------------------------------------------------------------

    def has_members(self):
        return len(self) > 0


    def uses_external_sht(self):
        for exegete in self.__exegetes:
            if exegete.uses_external_sht():
                return True

        return False


    def interpretation(self, text, internal_sht_sample, external_sht_sample):
        interpretations = OrderedDict()

        for exegete in self.__exegetes:
            sht_sample = external_sht_sample if exegete.uses_external_sht() else internal_sht_sample
            interpretations[exegete.name()] = exegete.interpretation(text, sht_sample.humid)

        return interpretations


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        exegetes = '[' + ', '.join(str(exegete) for exegete in self.__exegetes) + ']'

        return "ExegeteCollection:{exegetes:%s}" % exegetes
