"""
Created on 06 Nov 2020

@author: Jade Page (jade.page@southcoastscience.com)

"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class BylineList(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_bylines_list"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        byline_list = jdict.get('byline_list')

        return BylineList(byline_list)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, byline_list):
        """
        Constructor
        """
        super().__init__()

        self.__byline_list = byline_list

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def byline_list(self):
        return self.__byline_list

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['byline_list'] = self.__byline_list

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "UptimeList:{byline_list:%s}" %  \
               self.byline_list
