"""
Created on 21 Jan 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class Indexable(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    @property
    def index(self):                                # a scalar that is unique in the dataset
        pass


# --------------------------------------------------------------------------------------------------------------------

class Dataset(object):
    """
    classdocs
    """
    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__items = OrderedDict()                # dict of index: Indexable


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, item: Indexable):
        self.__items[item.index] = item


    def extend(self, items):
        for item in items:
            self.add(item)


    def is_invalidated_by_item(self, item: Indexable):
        try:
            return item != self.__items[item.index]

        except KeyError:
            return True


    # TODO: test for items in this dataset that are not in the client dataset


    # ----------------------------------------------------------------------------------------------------------------

    def items(self):
        return self.__items.items()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Dataset:{items:%s}" % Str.collection(self.__items)

