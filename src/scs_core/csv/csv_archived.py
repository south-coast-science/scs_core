"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from abc import abstractmethod

from scs_core.csv.csv_reader import CSVReader


# --------------------------------------------------------------------------------------------------------------------

class CSVArchived(object):
    """
    classdocs
    """

    _retrieved = None                # MUST be overridden by concrete classes!

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def retrieve(cls):
        reader = CSVReader(filename=cls.archive_location(), cast=False)

        try:
            for row in reader.rows:
                instance = cls.construct_from_jdict(json.loads(row))
                cls._retrieved[instance.pk] = instance

        finally:
            reader.close()


    @classmethod
    def instances(cls):
        return cls._retrieved.values()


    @classmethod
    def instance(cls, pk):
        if pk not in cls._retrieved:
            return None

        return cls._retrieved[pk]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def archive_location(cls):
        return ''


    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, _):
        return None


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def pk(self):
        return None
