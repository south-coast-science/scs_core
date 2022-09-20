"""
Created on 27 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import re

from collections import OrderedDict
from copy import deepcopy

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PathDict(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def union(*pairs):
        union = PathDict()

        for name, value in pairs:
            if value is not None:
                union.append(name, value)

        return union


    @staticmethod
    def sub_path_includes_path(sub_path, path):
        sub_path_nodes = [node[0] for node in re.findall(r'([^.:]+)([.:]*)', sub_path)]
        path_nodes = [node[0] for node in re.findall(r'([^.:]+)([.:]*)', path)]

        for i in range(len(sub_path_nodes)):
            try:
                if sub_path_nodes[i] != path_nodes[i]:
                    return False
            except IndexError:
                return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jstr(cls, jstr, sort_paths=()):
        try:
            jdict = json.loads(jstr)
        except ValueError:
            return None

        return cls(dictionary=jdict, sort_paths=sort_paths)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, dictionary=None, sort_paths=()):
        """
        Constructor
        """
        self.__dictionary = OrderedDict() if dictionary is None else dictionary
        self.__sort_paths = sort_paths


    def __len__(self):
        return len(self.__dictionary)


    def __lt__(self, other):
        for sort_path in self.__sort_paths:
            value = self.node(sub_path=sort_path)
            other_value = other.node(sub_path=sort_path)

            if value < other_value:
                return True

            if value > other_value:
                return False

        return False


    # -----------------------------------------------------------------------------------------------------------------
    # source...

    # Tests whether a leaf node path is present...

    def has_path(self, path):
        return path in self.paths()


    # Tests whether a leaf node or internal path is present...

    def has_sub_path(self, sub_path=None):
        if sub_path is None:
            return True

        try:
            self.node(sub_path)
            return True

        except (KeyError, TypeError):
            return False


    # Returns all the leaf node paths...

    def paths(self, sub_path=None):
        node = self if sub_path is None else PathDict(self.node(sub_path))

        return node.__paths(node.__dictionary, sub_path)


    # Returns a leaf node or internal node...

    def node(self, sub_path=None):
        if sub_path is None:
            return self.__dictionary

        try:
            return self.__node(self.__dictionary, re.split(r"[.:]", sub_path))

        except (KeyError, TypeError):
            raise KeyError(sub_path)


    # Appends or replaces value at sub_path...

    def append(self, sub_path, value):
        nodes = re.findall('([^.:]+)([.:]*)', sub_path)

        try:
            self.__append(self.__dictionary, nodes, value)

        except (KeyError, TypeError):
            raise KeyError(sub_path)


    # Sets an internal node to the given value...

    def set_node(self, sub_path, value):
        try:
            return self.__set_node(self.__dictionary, re.split(r"[.:]", sub_path), value)

        except (KeyError, TypeError):
            raise KeyError(sub_path)


    # ----------------------------------------------------------------------------------------------------------------
    # target...

    # Copies from other at sub_path...

    def copy(self, other, sub_path=None):
        if sub_path is None:
            self.__dictionary = deepcopy(other.__dictionary)
            return

        nodes = re.findall('([^.:]+)([.:]*)', sub_path)

        try:
            self.__append(self.__dictionary, nodes, other.node(sub_path))

        except KeyError:
            raise KeyError(sub_path)


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
        value = container[key]                      # raises TypeError if container is None

        # leaf...
        if len(nodes) == 1:
            return value

        # deep...
        return self.__node(value, nodes[1:])


    def __set_node(self, container, nodes, value):
        # key...
        if isinstance(container, list):
            try:
                key = int(nodes[0])

            except ValueError:
                raise KeyError(nodes[0])            # a non-integer key on an array is a KeyError

        else:
            key = nodes[0]

        # value...
        container[key] = value

        # leaf...
        if len(nodes) == 1:
            return value

        # deep...
        return self.__set_node(value, nodes[1:], value)


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

            while key >= len(container):
                container.append(None)

            if container[key] is None:
                container[key] = [] if separator == ':' else OrderedDict()

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


    @property
    def sort_paths(self):
        return self.__sort_paths


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.__dictionary


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PathDict:{sort_paths:%s, dictionary:%s}" % (self.sort_paths, self.node())
