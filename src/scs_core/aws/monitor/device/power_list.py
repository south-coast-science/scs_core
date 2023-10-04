"""
Created on 23 Nov 2020

@author: Jade Page (jade.page@southcoastscience.com)

"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class PowerList(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_power_list"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        power_list = jdict.get('power_list')

        return PowerList(power_list)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, power_list):
        """
        Constructor
        """
        super().__init__()

        self.__power_list = power_list

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def power_list(self):
        return self.__power_list

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['power_list'] = self.__power_list

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PowerList:{power_list:%s}" %  \
               self.power_list
