'''
Created on 27 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

import json

from collections import OrderedDict
from copy import deepcopy

from scs_core.common.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PathDict(JSONable):
    '''
    classdocs
    '''

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jstr(cls, jstr):
        try:
            jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
        except:
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
        except:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, dict = None):
        '''
        Constructor
        '''
        self.__dict = dict if dict else OrderedDict()


    # -----------------------------------------------------------------------------------------------------------------
    # source...

    def has_path(self, path):
        return self.__has_path(self.__dict, path.split("."))


    def node(self, *paths):
        if not paths:
            return self.__dict

        values = tuple([self.__node(self.__dict, path.split(".")) for path in paths])

        return values[0] if len(values) == 1 else values


    # ----------------------------------------------------------------------------------------------------------------
    # target...

    def copy(self, other, *paths):
        if not paths:
            self.__dict = deepcopy(other.__dict)
            return

        for path in paths:
            self.__append(self.__dict, path.split("."), other.node(path))


    def append(self, path, value):
        self.__append(self.__dict, path.split("."), value)


    # ----------------------------------------------------------------------------------------------------------------

    def __has_path(self, dictionary, nodes):
        key = nodes[0]

        if not key in dictionary:
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
            if not key in dictionary:
                dictionary[key] = []

            dictionary[key].append(value)

        # object...
        else:
            if not key in dictionary:
                dictionary[key] = OrderedDict()

            self.__append(dictionary[key], nodes[1:], value)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__dict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PathDict:{dict:%s}" % (self.node())
