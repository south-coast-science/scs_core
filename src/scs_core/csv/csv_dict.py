"""
Created on 21 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import re

from collections import OrderedDict

from scs_core.data.path_dict import PathDict
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class CSVDict(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jstr(cls, jstr):
        try:
            jdict = json.loads(jstr, object_hook=OrderedDict)

        except ValueError:
            return None

        return CSVDict(PathDict(jdict))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path_dict):
        """
        Constructor
        """
        self.__path_dict = path_dict


    def __len__(self):
        return len(self.__path_dict)


    # ----------------------------------------------------------------------------------------------------------------

    def row(self, paths):
        return tuple(self.__path_dict.node(path) if self.__path_dict.has_path(path) else None for path in paths)


    # ----------------------------------------------------------------------------------------------------------------

    def paths(self):
        return self.__path_dict.paths()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def dictionary(self):
        return self.__path_dict.collection


    @property
    def header(self):
        return CSVHeader.construct_from_paths(self.__path_dict.paths())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVDict:{path_dict:%s}" % self.__path_dict


# --------------------------------------------------------------------------------------------------------------------

class CSVHeader(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_paths(cls, paths):
        if len(paths) != len(set(paths)):
            raise ValueError(paths)                 # duplicate column names

        cells = [CSVHeaderCell.construct_from_path(path) for path in paths]

        return CSVHeader(cells)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cells):
        """
        Constructor
        """
        self.__cells = cells


    def __len__(self):
        return len(self.__cells)


    # ----------------------------------------------------------------------------------------------------------------

    def as_dict(self, row):
        if len(row) != len(self):
            raise ValueError("unmatched lengths: header: %s row: %s" % (list(self.paths()), row))

        dictionary = OrderedDict()

        for i in range(len(row)):
            try:
                self.__cells[i].insert(dictionary, row[i])
            except TypeError:
                raise CSVHeaderError(self.__cells[i - 1].path, self.__cells[i].path)        # clashing column names

        return dictionary


    # ----------------------------------------------------------------------------------------------------------------

    def paths(self):
        return tuple(cell.path for cell in self.__cells)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVHeader:{cells:%s}" % Str.collection(self.__cells)


# --------------------------------------------------------------------------------------------------------------------

class CSVHeaderCell(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_path(cls, path):
        p = re.compile(r'([^.:]+)([.:])?')
        nodes = p.findall(path)

        if not nodes:
            raise KeyError(path)

        return CSVHeaderCell(nodes)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, nodes):
        """
        Constructor
        """
        self.__nodes = nodes


    def __len__(self):
        return len(self.__nodes)


    # ----------------------------------------------------------------------------------------------------------------

    def insert(self, container, value, i=0):
        if isinstance(container, list):
            key = int(self._name(i))

            # leaf node...
            if self._is_leaf_node(i):
                container.append(value)
                return

            # sub-container...
            item = [] if self._is_list(i) else OrderedDict()

            while len(container) < key + 1:
                container.append(item)

        else:
            key = self._name(i)

            # leaf node...
            if self._is_leaf_node(i):
                container[key] = value
                return

            # sub-container...
            item = [] if self._is_list(i) else OrderedDict()

            if key not in container:
                container[key] = item       # TypeError if key identifies a leaf node and item is an internal node

        self.insert(container[key], value, i + 1)


    # ----------------------------------------------------------------------------------------------------------------

    def _name(self, i):
        return self.__nodes[i][0]


    def _is_list(self, i):
        return self.__nodes[i][1] == ':'


    def _is_leaf_node(self, i):
        return i == len(self) - 1


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        nodes = [node[0] + node[1] for node in self.__nodes]

        return ''.join(nodes)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVHeaderCell:{nodes:%s}" % self.__nodes


# --------------------------------------------------------------------------------------------------------------------

class CSVHeaderError(TypeError):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, left, right):
        """
        Constructor
        """
        self.__left = left
        self.__right = right


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def left(self):
        return self.__left


    @property
    def right(self):
        return self.__right


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVHeaderError:{left:%s, right:%s}" % (self.left, self.right)
