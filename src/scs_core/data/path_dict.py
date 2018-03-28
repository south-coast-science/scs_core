"""
Created on 27 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict
from copy import deepcopy

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PathDict(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jstr(cls, jstr):
        try:
            jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
        except ValueError:
            return None

        return PathDict(jdict)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __is_list_item(cls, item, nodes):
        if not isinstance(item, list):
            return False

        return cls.__is_list_path(nodes)


    @classmethod
    def __is_list_path(cls, nodes):
        if len(nodes) != 2:
            return False

        try:
            leaf_node = float(nodes[1])
            return leaf_node.is_integer()
        except ValueError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, dictionary=None):
        """
        Constructor
        """
        self.__dictionary = dictionary if dictionary else OrderedDict()


    # -----------------------------------------------------------------------------------------------------------------
    # source...

    def has_path(self, path):
        if path is None:
            return True

        try:
            return self.__has_path(self.__dictionary, path.split("."))

        except TypeError:
            return False


    def node(self, path=None):
        if path is None:
            return self.__dictionary

        return self.__node(self.__dictionary, path.split("."))


    # ----------------------------------------------------------------------------------------------------------------
    # target...

    def copy(self, other, path=None):
        if path is None:
            self.__dictionary = deepcopy(other.__dictionary)
            return

        self.__append(self.__dictionary, path.split("."), other.node(path))


    def append(self, path, value):
        self.__append(self.__dictionary, path.split("."), value)


    # ----------------------------------------------------------------------------------------------------------------

    def __has_path(self, dictionary, nodes):
        key = nodes[0]

        if key not in dictionary:
            return False

        # scalar...
        if len(nodes) == 1:
            return True

        item = dictionary[key]

        # list...
        if PathDict.__is_list_item(item, nodes):
            index = int(nodes[1])
            return 0 <= index < len(item)

        # object...
        return self.__has_path(item, nodes[1:])


    def __node(self, dictionary, nodes):
        key = nodes[0]

        item = dictionary[key]

        # scalar...
        if len(nodes) == 1:
            return item

        # list...
        if PathDict.__is_list_item(item, nodes):
            index = int(nodes[1])
            return item[index]

        # object...
        return self.__node(item, nodes[1:])


    def __append(self, dictionary, nodes, value):
        key = nodes[0]

        # scalar...
        if len(nodes) == 1:
            dictionary[key] = deepcopy(value)

        # list...
        elif PathDict.__is_list_path(nodes):
            if key not in dictionary:
                dictionary[key] = []

            dictionary[key].append(value)

        # object...
        else:
            if key not in dictionary:
                dictionary[key] = OrderedDict()

            self.__append(dictionary[key], nodes[1:], value)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__dictionary


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PathDict:{dictionary:%s}" % (self.node())
