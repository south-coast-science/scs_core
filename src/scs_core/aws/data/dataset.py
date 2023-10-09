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
    def references(self, other):
        pass


    @abstractmethod
    def copy_pk(self, other):
        pass


    @abstractmethod
    def save(self, db_username):
        pass


    @abstractmethod
    def delete(self, db_username):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def index(self):                                        # a scalar that is unique within the dataset
        return None


    @property
    @abstractmethod
    def last_updated(self):                                 # LocalizedDatetime
        return None


# --------------------------------------------------------------------------------------------------------------------

class Dataset(object):
    """
    classdocs
    """
    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, db_username, latest_import, simulate=False):
        """
        Constructor
        """
        self.__db_username = db_username                    # string
        self.__latest_import = latest_import                # LocalizedDatetime
        self.__simulate = simulate                          # bool

        self.__items = OrderedDict()                        # dict of index: Indexable
        self.__logger = Logging.getLogger()


    def __len__(self):
        return len(self.__items)


    def __contains__(self, item):
        for dataset_item in self.__items.values():
            # print("item: %s" % item)
            # print("dataset_item: %s" % dataset_item)
            if dataset_item.references(item):
                return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def clear(self):
        self.__items = OrderedDict()


    def add(self, item: DatasetItem):
        self.__items[item.index] = item


    def extend(self, items):
        for item in items:
            self.add(item)


    def update_with(self, item: DatasetItem, insert_only=False):
        try:
            retrieved_item = self.__items[item.index]

            if insert_only:
                return

            # no changes...
            if item == retrieved_item:
                return

            # AWS item is newer - ignore old-world item...
            if self.latest_import and retrieved_item.last_updated > self.latest_import:
                self.__logger.warn('WARNING: old-world item ignored: %s' % item)
                return

            # old-world item is newer...
            item.copy_pk(retrieved_item)

            if not self.simulate:
                item.save(self.db_username)

            self.__items[item.index] = item
            self.__logger.warn('updated: %s' % item)

        except KeyError:
            # no AWS item...
            if not self.simulate:
                item.save(self.db_username)

            self.__items[item.index] = item
            self.__logger.warn('inserted: %s' % item)


    def delete_unreferenced(self, references):
        for index, item in list(self.__items.items()):
            if item in references:
                continue

            if not self.simulate:
                item.delete(self.db_username)

            del self.__items[index]
            self.__logger.warn("deleted: %s" % item)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def db_username(self):
        return self.__db_username


    @property
    def latest_import(self):
        return self.__latest_import


    @property
    def simulate(self):
        return self.__simulate


    def item(self, index):
        return self.__items[index]                          # may raise KeyError


    def keys(self):
        return self.__items.keys()


    def values(self):
        return self.__items.values()


    def items(self):
        return self.__items.items()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Dataset:{db_username:%s, latest_import:%s, simulate:%s, items:%s}" % \
               (self.db_username, self.latest_import, self.simulate, Str.collection(self.__items))
