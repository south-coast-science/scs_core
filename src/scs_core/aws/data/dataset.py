"""
Created on 21 Jan 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.data.str import Str
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class DatasetItem(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def copy_id(self, other):
        pass


    @abstractmethod
    def save(self, db_user):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def index(self):                            # a scalar that is unique within the dataset
        return None


    @property
    @abstractmethod
    def latest_update(self):                    # LocalizedDatetime
        return None


# --------------------------------------------------------------------------------------------------------------------

class Dataset(object):
    """
    classdocs
    """
    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, db_user, latest_import):
        """
        Constructor
        """
        self.__db_user = db_user                            # string
        self.__latest_import = latest_import                # LocalizedDatetime
        self.__items = OrderedDict()                        # dict of index: Indexable

        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, item: DatasetItem):
        self.__items[item.index] = item


    def extend(self, items):
        for item in items:
            self.add(item)


    def update_with(self, item: DatasetItem):
        try:
            retrieved_item = self.__items[item.index]

            if item == retrieved_item:
                return

            self.__logger.error('retrieved: %s' % retrieved_item)
            self.__logger.error('    given: %s' % item)

            if retrieved_item.latest_update > self.latest_import:
                self.__logger.error('WARNING: item discarded: %s' % item)
                return

            item.copy_id(retrieved_item)
            item.save(self.db_user)
            self.__logger.error('updated: %s' % item)
            self.__items[item.index] = item

        except KeyError:
            item.save(self.db_user)
            self.__logger.error('inserted: %s' % item)
            self.__items[item.index] = item


    # TODO: check for items in retrieved set that are not in the old-world set


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def db_user(self):
        return self.__db_user


    @property
    def latest_import(self):
        return self.__latest_import


    def item(self, index):
        return self.__items[index]                  # may raise KeyError


    def items(self):
        return self.__items.items()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Dataset:{db_user:%s, latest_import:%s, items:%s}" % \
               (self.db_user, self.latest_import, Str.collection(self.__items))
