"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

specifies which sensor interface board is present, if any

example JSON:
{"model": "DFE", "inf": "/home/scs/SCS/pipes/lambda-model-gas-s1.uds"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class InterfaceConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "interface_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        model = jdict.get('model')

        return cls(model)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, model):
        """
        Constructor
        """
        super().__init__()

        self.__model = model                                        # string


    def __eq__(self, other):
        try:
            return self.model == other.model

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    # noinspection PyMethodMayBeStatic
    def interface(self):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__model


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['model'] = self.model

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "InterfaceConf(core):{model:%s}" % self.model
