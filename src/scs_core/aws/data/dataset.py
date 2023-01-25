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


    @abstractmethod
    def delete(self, db_user):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def index(self):                                    # a scalar that is unique within the dataset
        return None


    @property
    @abstractmethod
    def last_updated(self):                            # LocalizedDatetime
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
        self.__db_user = db_user                        # string
        self.__latest_import = latest_import            # LocalizedDatetime

        self.__items = OrderedDict()                    # dict of index: Indexable
        self.__references = set()                       # set of scalar

        self.__logger = Logging.getLogger()


    def __len__(self):
        return len(self.__items)


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, item: DatasetItem):
        self.__items[item.index] = item


    def extend(self, items):
        for item in items:
            self.add(item)


    def update_with(self, item: DatasetItem):
        self.__references.add(item.index)

        try:
            retrieved_item = self.__items[item.index]

            # no changes...
            if item == retrieved_item:
                return

            # AWS item is newer - discard MFR item...
            if retrieved_item.last_updated > self.latest_import:
                self.__logger.info('WARNING: item update discarded: %s' % item)
                return

            # old-world item is newer...
            item.copy_id(retrieved_item)
            item.save(self.db_user)
            self.__logger.info('updated: %s: %s' % (item.index, item))
            self.__items[item.index] = item

        except KeyError:
            # no AWS item...
            item.save(self.db_user)
            self.__logger.info('inserted: %s: %s' % (item.index, item))
            self.__items[item.index] = item


    def delete_unreferenced(self):
        for index, item in self.__items.items():
            if index not in self.references:
                item.delete(self.db_user)
                self.__logger.info('deleted: %s: %s' % (item.index, item))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def db_user(self):
        return self.__db_user


    @property
    def latest_import(self):
        return self.__latest_import


    def item(self, index):
        return self.__items[index]                  # may raise KeyError


    def keys(self):
        return self.__items.keys()


    def items(self):
        return self.__items.items()


    @property
    def references(self):
        return self.__references


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Dataset:{db_user:%s, latest_import:%s, items:%s, references:%s}" % \
               (self.db_user, self.latest_import, Str.collection(self.__items), self.references)
