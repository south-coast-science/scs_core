"""
Created on 2 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class AbstractTopic(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, name, description, is_public, info):
        """
        Constructor
        """
        self.__path = path                          # string
        self.__name = name                          # string
        self.__description = description            # string

        self.__is_public = is_public                # bool

        self.__info = info                          # TopicInfo


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.path is not None:
            jdict['topic'] = self.path

        jdict['name'] = self.name
        jdict['description'] = self.description

        jdict['public'] = self.is_public

        jdict['topic-info'] = self.info

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    @property
    def name(self):
        return self.__name


    @property
    def description(self):
        return self.__description


    @property
    def is_public(self):
        return self.__is_public


    @property
    def info(self):
        return self.__info
