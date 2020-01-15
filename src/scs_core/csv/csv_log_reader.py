"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


import csv
import sys
import time

from scs_core.csv.csv_dict import CSVDict

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class CSVLogReader(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, log):
        """
        Constructor
        """
        self.__host = host                              # Host
        self.__log = log                                # CSVLog


    # ----------------------------------------------------------------------------------------------------------------

    def read(self, from_datetime, to_datetime=None):
        self.__months(from_datetime, to_datetime)


    # ----------------------------------------------------------------------------------------------------------------

    def __months(self, from_datetime, to_datetime):
        months = []

        for month in Filesystem.ls(self.log.root_path):
            print(month)

        return []



    # ----------------------------------------------------------------------------------------------------------------

    @property
    def log(self):
        return self.__log


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogReader:{log:%s}" % self.log
