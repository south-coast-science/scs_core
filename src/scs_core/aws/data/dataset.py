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

    @property
    @abstractmethod
    def index(self):                            # a scalar that is unique within the dataset
        return None


    @property
    @abstractmethod
    def latest_update(self):                    # LocalizedDatetime
        return None


    @abstractmethod
    def copy_id(self, other):
        pass


    def save(self, db_user):
        raise NotImplementedError


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


    def revalidate(self, item: DatasetItem):        # TODO: add to / update dataset?
        self.__logger.error('item: %s' % item)

        try:
            retrieved_item = self.__items[item.index]

            if item == retrieved_item:
                self.__logger.error('invalidated: False (equals)')
                return

            if retrieved_item.latest_update > self.latest_import:
                self.__logger.error('invalidated: False (retrieved is younger)')
                self.__logger.error('retrieved (kept): %s' % retrieved_item)
                return

            self.__logger.error('invalidated: True (retrieved is older)')
            item.id = retrieved_item.id
            item.save(self.db_user)
            self.__items[item.index] = item

        except KeyError:
            self.__logger.error('invalidated: True (retrieved is absent)')
            item.save(self.db_user)
            self.__items[item.index] = item


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def db_user(self):
        return self.__db_user


    @property
    def latest_import(self):
        return self.__latest_import


    def items(self):
        return self.__items.items()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Dataset:{db_user:%s, latest_import:%s, items:%s}" % \
               (self.db_user, self.latest_import, Str.collection(self.__items))
