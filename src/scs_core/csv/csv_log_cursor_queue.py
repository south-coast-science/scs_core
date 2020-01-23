"""
Created on 20 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.csv.csv_log import CSVLog, CSVLogFile
from scs_core.csv.csv_reader import CSVReader

from scs_core.data.json import JSONable
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class CSVLogCursorQueue(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_for_log(cls, log: CSVLog, rec_field):                         # cursors are NOT live
        queue = OrderedDict()

        for directory_path in cls.__directory_paths(log):
            for log_file in cls.__log_files(log, directory_path):
                cursor = CSVLogCursor.construct_for_log_file(log, log_file, rec_field)

                if cursor is not None:
                    queue[cursor.file_path] = cursor

        return cls(queue)


    @classmethod
    def __directory_paths(cls, log: CSVLog):
        from_directory = CSVLog.directory_name(log.timeline_start)

        for directory in Filesystem.ls(log.root_path):
            if directory.name < from_directory:
                continue

            yield directory.path()


    @staticmethod
    def __log_files(log: CSVLog, directory_path):
        for file in Filesystem.ls(directory_path):
            log_file = CSVLogFile.construct(file)

            if log_file.topic_name != log.topic_name:
                continue

            if log_file.created_datetime.date() < log.timeline_start.date():
                continue

            yield log_file


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        queue = OrderedDict()

        for cursor_jdict in jdict.get('queue'):
            cursor = CSVLogCursor.construct_from_jdict(cursor_jdict)
            queue[cursor.file_path] = cursor

        return cls(queue)


    # ----------------------------------------------------------------------------------------------------------------
    #

    def __init__(self, queue=None):
        """
        Constructor
        """
        self.__queue = OrderedDict() if queue is None else queue        # OrderedDict of CSVLogCursor


    def __len__(self):
        return len(self.__queue)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['queue'] = [cursor.as_json() for cursor in self.__queue.values()]

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def include(self, cursor):
        if cursor.is_live:
            for file_path in self.__queue.keys():
                self.__queue[file_path].is_live = False           # there shall only be one live file

        self.__queue[cursor.file_path] = cursor


    def pop(self):
        try:
            return self.__queue.popitem(last=False)[1]
        except KeyError:
            return None


    def queue(self):
        for cursor in self.__queue.values():
            yield cursor


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        queue = '[' + ', '.join(str(cursor) for cursor in self.__queue.values()) + ']'

        return "CSVLogCursorQueue:{queue:%s}" %  queue


# --------------------------------------------------------------------------------------------------------------------

class CSVLogCursor(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_for_log_file(cls, log: CSVLog, log_file, rec_field):          # cursor is NOT live
        reader = None
        row_number = 0

        try:
            reader = CSVReader.construct_for_file(log_file.path(), numeric_cast=False)

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

                if rec.datetime > log.timeline_start:
                    return cls(log_file.path(), row_number, False)

                row_number += 1

            return None

        finally:
            if reader is not None:
                reader.close()


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        file_path = jdict.get('file-path')
        row_number = jdict.get('row-number')
        is_live = jdict.get('is-live')

        return cls(file_path, row_number, is_live)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, file_path, row_number, is_live):
        """
        Constructor
        """
        self.__file_path = file_path                            # string
        self.__row_number = int(row_number)                     # int
        self.__is_live = bool(is_live)                          # bool


    def __eq__(self, other):
        return self.file_path == other.file_path


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['file-path'] = self.file_path
        jdict['row-number'] = self.row_number
        jdict['is-live'] = self.is_live

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def file_path(self):
        return self.__file_path


    @property
    def row_number(self):
        return self.__row_number


    @property
    def is_live(self):
        return self.__is_live


    @is_live.setter
    def is_live(self, is_live):
        self.__is_live = is_live


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogCursor:{file_path:%s, row_number:%s, is_live:%s}" %  \
               (self.file_path, self.row_number, self.is_live)
