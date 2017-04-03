"""
Created on 2 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import abstractmethod

from scs_core.data.json import JSONable


# TODO: is this the TopicSummary delivered by the API?

# --------------------------------------------------------------------------------------------------------------------

class AbstractTopic(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, name, description, is_public, topic_info):
        """
        Constructor
        """
        self.__path = path                          # string
        self.__name = name                          # string
        self.__description = description            # string

        self.__is_public = is_public                # bool

        self.__topic_info = topic_info              # TopicInfo


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def as_json(self):
        pass


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
    def topic_info(self):
        return self.__topic_info
