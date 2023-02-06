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


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, item: DatasetItem):
        self.__items[item.index] = item


    def extend(self, items):
        for item in items:
            self.add(item)


    def update_with(self, item: DatasetItem):
        try:
            retrieved_item = self.__items[item.index]

            # no changes...
            if item == retrieved_item:
                return

            # AWS item is newer - ignore old-world item...
            if retrieved_item.last_updated > self.latest_import:
                self.__logger.info('WARNING: old-world item ignored: %s' % item)
                return

            # old-world item is newer...
            item.copy_id(retrieved_item)

            if not self.__simulate:
                item.save(self.db_username)

            self.__logger.info('updated: %s' % item)
            self.__items[item.index] = item

        except KeyError:
            # no AWS item...
            if not self.__simulate:
                item.save(self.db_username)

            self.__logger.info('inserted: %s' % item)
            self.__items[item.index] = item


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
