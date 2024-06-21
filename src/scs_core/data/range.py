"""
Created on 20 Jun 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"CO": {"cnc": {"min": 104.2, "mid": 181.8, "max": 520.7, "full-range": 416.5, "upper-range": 338.9}
"""

from collections import OrderedDict


# --------------------------------------------------------------------------------------------------------------------

class Range(object):
    """
    classdocs
    """

    __EDGES = ['min', 'mid', 'max']

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, precision=1, prefix=None):
        """
        Constructor
        """
        self.__precision = int(precision)               # int
        self.__prefix = prefix                          # string
        self.__edges = OrderedDict()                    # dict of edge: float


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, path, value):
        try:
            prefix = path[:-4]
            edge = path[-3:]
        except KeyError:
            return

        if edge not in self.__EDGES:
            return

        if self.prefix is None or self.prefix != prefix:
            self.reset()
            self.__prefix = prefix

        self.__edges[edge] = float(value)


    def is_complete(self):
        for edge in self.__EDGES:
            if edge not in self.__edges:
                return False

        return True


    def reset(self):
        self.__prefix = None
        self.__edges = OrderedDict()


    # ----------------------------------------------------------------------------------------------------------------

    def full_range(self):
        path = '.'.join((self.prefix, 'full-range'))
        value = self.edges['max'] - self.edges['min']

        return path, round(value, self.__precision)


    def upper_range(self):
        path = '.'.join((self.prefix, 'upper-range'))
        value = self.edges['max'] - self.edges['mid']

        return path, round(value, self.__precision)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def prefix(self):
        return self.__prefix


    @property
    def edges(self):
        return self.__edges


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Range:{precision:%s, prefix:%s, edges:%s}" % \
                (self.__precision, self.prefix, self.edges)
