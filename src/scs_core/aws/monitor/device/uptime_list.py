"""
Created on 06 Nov 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class UptimeList(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_uptime_list"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        uptime_list = jdict.get('uptime_list')

        return UptimeList(uptime_list)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uptime_list):
        """
        Constructor
        """
        super().__init__()

        self.__uptime_list = uptime_list


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def uptime_list(self):
        return self.__uptime_list

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['uptime_list'] = self.__uptime_list

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UptimeList:{uptime_list:%s}" %  \
               self.uptime_list
