"""
Created on 21 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class CSVDict(object):

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def as_dict(cls, header, row):
        if len(header) != len(row):
            raise ValueError("unmatched lengths: header: %s row: %s" % (header, row))

        dictionary = OrderedDict()

        for i in range(len(header)):
            cls.__as_dict(header[i].strip().split("."), row[i], dictionary)

        return dictionary


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __as_dict(cls, nodes, cell, dictionary):
        key = nodes[0]

        # scalar...
        if len(nodes) == 1:
            dictionary[key] = cell
            return

        # list...
        if cls.__is_list_path(nodes):
            if key not in dictionary:
                dictionary[key] = []

            dictionary[key].append(cell)
            return

        # object...
        if key not in dictionary:
            dictionary[key] = OrderedDict()

        cls.__as_dict(nodes[1:], cell, dictionary[key])


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

    @classmethod
    def construct(cls, dictionary):
        return CSVDict(PathDict(dictionary))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path_dict):
        """
        Constructor
        """
        self.__path_dict = path_dict


    # ----------------------------------------------------------------------------------------------------------------

    def row(self, header):
        row = []
        for key in header:
            value = self.__path_dict.node(key) if self.__path_dict.has_path(key) else None
            row.append(value)

        return row


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def dictionary(self):
        return self.__path_dict.dictionary


    @property
    def header(self):
        return self.__path_dict.paths()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVDict:{path_dict:%s}" % self.__path_dict
