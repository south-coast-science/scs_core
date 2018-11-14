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

    @property
    def paths(self):
        return self.__paths(self.__dictionary)


    def has_path(self, path):
        if path is None:
            return True

        return path in self.paths


    def node(self, path=None):
        if path is None:
            return self.__dictionary

        return self.__node(self.__dictionary, re.split(r"[.:]", path))


    # ----------------------------------------------------------------------------------------------------------------
    # target...

    # Warning: copying nodes within arrays yields numerically-indexed dictionaries

    def copy(self, other, path=None):
        if path is None:
            self.__dictionary = deepcopy(other.__dictionary)
            return

        self.__append(self.__dictionary, re.split(r"[.:]", path), other.node(path))


    # Warning: appending within an array is only permitted within the array's existing bounds

    def append(self, path, value):
        self.__append(self.__dictionary, re.split(r"[.:]", path), value)


    # ----------------------------------------------------------------------------------------------------------------

    def __paths(self, container, prefix=None):
        if isinstance(container, list):
            separator = ':'
            keys = range(len(container))

        else:
            separator = '.'
            keys = container.keys()

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
                raise KeyError(nodes[0])

        else:
            key = nodes[0]

        # value...
        value = container[key]

        # scalar...
        if len(nodes) == 1:
            return value

        # dict or list...
        return self.__node(value, nodes[1:])


    def __append(self, container, nodes, value):
        # key...
        if isinstance(container, list):
            try:
                key = int(nodes[0])

            except ValueError:
                raise KeyError(nodes[0])

        else:
            key = nodes[0]

        # scalar...
        if len(nodes) == 1:
            container[key] = deepcopy(value)

        # dict or list...
        else:
            if key not in container:
                container[key] = OrderedDict()

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
