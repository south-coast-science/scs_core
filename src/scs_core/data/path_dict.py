"""
Created on 27 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import re
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

    def __init__(self, dictionary=None):
        """
        Constructor
        """
        self.__dictionary = OrderedDict() if dictionary is None else dictionary


    def __len__(self):
        return len(self.__dictionary)


    # -----------------------------------------------------------------------------------------------------------------
    # source...

    # Tests whether a leaf-node path is present...

    def has_path(self, path):
        return path in self.paths()


    # Tests whether a leaf-node or internal path is present...

    def has_sub_path(self, sub_path=None):
        if sub_path is None:
            return True

        try:
            self.node(sub_path)
            return True

        except KeyError:
            return False


    # Returns all the leaf-node paths...

    def paths(self, sub_path=None):
        node = self if sub_path is None else PathDict(self.node(sub_path))

        return node.__paths(node.__dictionary, sub_path)


    # Returns a leaf-node or internal node...

    def node(self, sub_path=None):
        if sub_path is None:
            return self.__dictionary

        return self.__node(self.__dictionary, re.split(r"[.:]", sub_path))


    # ----------------------------------------------------------------------------------------------------------------
    # target...

    def copy(self, other, sub_path=None):
        if sub_path is None:
            self.__dictionary = deepcopy(other.__dictionary)
            return

        self.__append(self.__dictionary, re.split(r"[.:]", sub_path), other.node(sub_path))


    def append(self, sub_path, value):
        nodes = re.findall('([^.:]+)([.:]*)', sub_path)

        self.__append(self.__dictionary, nodes, value)


    # ----------------------------------------------------------------------------------------------------------------

    def __paths(self, container, prefix=None):
        # dict...
        if isinstance(container, dict):
            separator = '.'
            keys = container.keys()

        # list...
        elif isinstance(container, list):
            separator = ':'
            keys = range(len(container))

        # scalar...
        else:
            return [prefix]

        prefix = prefix + separator if prefix else ''

        paths = []

        for key in keys:
            path = prefix + str(key)
            value = container[key]

            # dict...
            if isinstance(value, dict):
                paths.extend(self.__paths(value, path))

            # list...
            elif isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], (list, dict)):
                        paths.extend(self.__paths(value[i], path + ':' + str(i)))
                    else:
                        paths.append(path + ':' + str(i))

            # scalar...
            else:
                paths.append(path)

        return paths


    def __node(self, container, nodes):
        # key...
        if isinstance(container, list):
            try:
                key = int(nodes[0])

            except ValueError:
                raise KeyError(nodes[0])            # a non-integer key on an array is a KeyError

        else:
            key = nodes[0]

        # value...
        value = container[key]

        # leaf...
        if len(nodes) == 1:
            return value

        # deep...
        return self.__node(value, nodes[1:])


    def __append(self, container, nodes, value):
        # key...
        key = nodes[0][0]
        separator = nodes[0][1]

        # dict...
        if isinstance(container, dict):
            if key not in container:
                container[key] = [] if separator == ':' else OrderedDict()

        # list...
        elif isinstance(container, list):
            try:
                key = int(key)
            except ValueError:
                raise KeyError(key)

            if key >= len(container):
                container.append([] if separator == ':' else OrderedDict())
                key = len(container) - 1

        # leaf...
        if len(nodes) == 1:
            container[key] = deepcopy(value)
            return

        # deep...
        self.__append(container[key], nodes[1:], value)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def dictionary(self):
        return self.node()


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__dictionary


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PathDict:{dictionary:%s}" % (self.node())
