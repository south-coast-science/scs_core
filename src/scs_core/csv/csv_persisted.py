"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from abc import abstractmethod

from scs_core.csv.csv_reader import CSVReader


# --------------------------------------------------------------------------------------------------------------------

class CSVPersisted(object):
    """
    classdocs
    """

    _persisted = None                # MUST be overridden by concrete classes!

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls):
        reader = CSVReader(filename=cls.persistence_location(), cast=False)

        try:
            for row in reader.rows:
                instance = cls.construct_from_jdict(json.loads(row))
                cls._persisted[instance.pk] = instance

        finally:
            reader.close()


    @classmethod
    def instances(cls):
        return cls._persisted.values()


    @classmethod
    def find(cls, pk):
        if pk not in cls._persisted:
            return None

        return cls._persisted[pk]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def persistence_location(cls):
        return ''


    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, _):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def pk(self):
        return None
