"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.csv.csv_log import CSVLog, CSVLogFile
from scs_core.csv.csv_reader import CSVReader

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class CSVLogReader(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, log, empty_string_as_null=True):
        """
        Constructor
        """
        self.__log = log                                            # CSVLog
        self.__empty_string_as_null = empty_string_as_null          # bool


    # ----------------------------------------------------------------------------------------------------------------

    def log_files(self):
        for directory_path in self.__directory_paths():
            for log_file in self.__log_files(directory_path):
                yield log_file


    def documents(self, log_file, rec_field):
        reader = None

        try:
            reader = CSVReader(filename=log_file.path(), empty_string_as_null=self.__empty_string_as_null)

            for row in reader.rows():
                try:
                    datum = json.loads(row, object_pairs_hook=OrderedDict)
                except ValueError:
                    continue

                if rec_field not in datum:
                    raise KeyError(rec_field)

                rec = LocalizedDatetime.construct_from_iso8601(datum[rec_field])

                if rec is None:
                    raise ValueError(datum[rec_field])

                if rec.datetime <= self.__log.timeline_start:
                    continue

                yield datum

        finally:
            if reader is not None:
                reader.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __directory_paths(self):
        from_directory = CSVLog.directory_name(self.__log.timeline_start)

        for directory in Filesystem.ls(self.__log.root_path):
            if directory.name < from_directory:
                continue

            yield directory.path()


    def __log_files(self, directory_path):
        for file in Filesystem.ls(directory_path):
            log_file = CSVLogFile.construct(file)

            if log_file.topic_name != self.__log.topic_name:
                continue

            if log_file.created_datetime.date() < self.__log.timeline_start.date():
                continue

            yield log_file


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogReader:{log:%s, empty_string_as_null:%s}" % (self.__log, self.__empty_string_as_null)
