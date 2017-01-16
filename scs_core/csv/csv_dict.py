'''
Created on 21 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from collections import OrderedDict


# TODO: deal with numeric index dictionaries

# --------------------------------------------------------------------------------------------------------------------

class CSVDict(object):

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def as_dict(cls, header, row):
        dictionary = OrderedDict()

        for i in range(len(header)):
            cls.__as_dict(header[i].split("."), row[i], dictionary)

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
            if not key in dictionary:
                dictionary[key] = []

            dictionary[key].append(cell)
            return

        # object...
        if not key in dictionary:
            dictionary[key] = OrderedDict()

        cls.__as_dict(nodes[1:], cell, dictionary[key])


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

    def __init__(self, dictionary):
        '''
        Constructor
        '''
        self.__dictionary = dictionary


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def dictionary(self):
        return self.__dictionary


    @property
    def header(self):
        return self.__header(self.__dictionary)


    @property
    def row(self):
        return self.__row(self.__dictionary)


    # ----------------------------------------------------------------------------------------------------------------

    def __header(self, dictionary, prefix = None):
        lprefix = prefix + '.' if prefix else ''

        header = []
        for key in dictionary:
            # object...
            if isinstance(dictionary[key], dict):
                header.extend(self.__header(dictionary[key], lprefix + key))

            # list...
            elif isinstance(dictionary[key], list):
                header.extend([lprefix + key + '.' + str(i) for i in range(len(dictionary[key]))])

            # scalar...
            else:
                header.append(lprefix + key)

        return header


    def __row(self, dictionary):
        row = []
        for key in dictionary:
            # object...
            if isinstance(dictionary[key], dict):
                row.extend(self.__row(dictionary[key]))

            # list...
            elif isinstance(dictionary[key], list):
                row.extend(dictionary[key])

            # scalar...
            else:
                row.append(dictionary[key])

        return row


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVDict:{dictionary:%s}" % self.dictionary
