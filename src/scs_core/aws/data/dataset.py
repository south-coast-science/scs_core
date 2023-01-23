"""
Created on 21 Jan 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.data.str import Str
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class Indexable(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def index(self):                                # a scalar that is unique in the dataset
        return None


# --------------------------------------------------------------------------------------------------------------------

class Dataset(object):
    """
    classdocs
    """
    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, latest_import):
        """
        Constructor
        """
        self.__latest_import = latest_import                # LocalizedDatetime
        self.__items = OrderedDict()                        # dict of index: Indexable

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, item: Indexable):
        self.__items[item.index] = item


    def extend(self, items):
        for item in items:
            self.add(item)


    def is_invalidated_by_item(self, item: Indexable):
        try:
            retrieved_item = self.__items[item.index]

            if item == retrieved_item:
                self.__logger.error('invalidated: False (equals)')
                return False

            if retrieved_item.latest_update > self.latest_import:
                self.__logger.error('retrieved (kept): %s' % retrieved_item)
                self.__logger.error('imported (discarded): %s' % item)
                return False

            else:
                self.__logger.error('invalidated: True (old)')
                return True

        except KeyError:
            self.__logger.error('invalidated: True (absent)')
            return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def latest_import(self):
        return self.__latest_import


    def items(self):
        return self.__items.items()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Dataset:{latest_import:%s, items:%s}" % (self.__latest_import, Str.collection(self.__items))

