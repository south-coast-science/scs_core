"""
Created on 16 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import csv
import json

from collections import OrderedDict

from scs_core.csv.csv_dict import CSVDict

from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class CSVLogger(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, log):
        """
        Constructor
        """
        self.__log = log

        self.__header = None
        self.__file = None


    # ----------------------------------------------------------------------------------------------------------------

    def write(self, jstr):
        if jstr is None:
            return

        if self.log is None:
            return

        jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
        datum = CSVDict(jdict)

        if not self.__file:
            self.__open_file()

        if not self.log.in_timeline(LocalizedDatetime.now()):
            self.close()
            self.__open_file()

        if not self.__header:
            self.__header = datum.header
            self.__writer.writerow(self.__header)

        self.__writer.writerow(datum.row)
        self.__file.flush()


    def close(self):
        if self.__file:
            self.__file.close()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def log(self):
        return self.__log


    # ----------------------------------------------------------------------------------------------------------------

    def __open_file(self):
        self.log.timeline_start = LocalizedDatetime.now()

        self.log.mkdir()

        self.__file = open(self.log.abs_file_name(), "w")
        self.__writer = csv.writer(self.__file, quoting=csv.QUOTE_MINIMAL)

        if self.__header:
            self.__writer.writerow(self.__header)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogger:{log:%s}" % self.log
