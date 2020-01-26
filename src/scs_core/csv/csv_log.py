"""
Created on 12 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import pytz
import re

from datetime import datetime as dt

from scs_core.sys.filesystem import Filesystem, File


# --------------------------------------------------------------------------------------------------------------------

class CSVLog(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def directory_name(datetime):
        if datetime is None:
            raise ValueError("datetime may not be None")

        return "%04d-%02d" % (datetime.year, datetime.month)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, root_path, topic_name, tag=None, timeline_start=None):
        """
        Constructor
        """
        self.__root_path = root_path                        # string
        self.__topic_name = topic_name                      # string
        self.__tag = tag                                    # string

        self.__timeline_start = timeline_start              # datetime


    # ----------------------------------------------------------------------------------------------------------------

    def cursor_queue(self, rec_field):
        # late import...
        from scs_core.csv.csv_log_cursor_queue import CSVLogCursorQueue

        return CSVLogCursorQueue.construct_for_log(self, rec_field)             # cursors are NOT live


    # ----------------------------------------------------------------------------------------------------------------

    def mkdir(self):
        Filesystem.mkdir(self.directory_path())


    def directory_path(self):
        return os.path.join(self.root_path, self.directory_name(self.timeline_start))


    def file_path(self):
        return os.path.join(self.directory_path(), CSVLogFile.name(self.timeline_start, self.topic_name, self.tag))


    def in_timeline(self, localised_datetime):
        if self.timeline_start is None:
            return False

        utc_localised_datetime = localised_datetime.utc()

        return utc_localised_datetime.datetime.date() == self.__timeline_start.date()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def root_path(self):
        return self.__root_path


    @property
    def topic_name(self):
        return self.__topic_name


    @property
    def tag(self):
        return self.__tag


    @tag.setter
    def tag(self, tag):
        self.__tag = tag


    @property
    def timeline_start(self):
        return self.__timeline_start


    @timeline_start.setter
    def timeline_start(self, localised_timeline_start):
        self.__timeline_start = localised_timeline_start.utc_datetime


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLog:{root_path:%s, tag:%s, topic_name:%s, timeline_start:%s}" % \
               (self.root_path, self.tag, self.topic_name, self.timeline_start)


# --------------------------------------------------------------------------------------------------------------------

class CSVLogFile(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def name(datetime, topic_name, tag=None):
        if datetime is None:
            raise ValueError("datetime may not be None")

        if tag is None:
            return "%s-%4d-%02d-%02d-%02d-%02d-%02d.csv" % \
                   (topic_name, datetime.year, datetime.month, datetime.day,
                    datetime.hour, datetime.minute, datetime.second)

        return "%s-%s-%4d-%02d-%02d-%02d-%02d-%02d.csv" % \
               (tag, topic_name, datetime.year, datetime.month, datetime.day,
                datetime.hour, datetime.minute, datetime.second)


    @classmethod
    def construct(cls, file: File):
        match = re.match(r'^(.+-)?([^-]+)-([\d]{4})-([\d]{2})-([\d]{2})-([\d]{2})-([\d]{2})-([\d]{2})\.csv',
                         file.name)

        if not match:
            return None

        fields = match.groups()

        # fields...
        tag = None if fields[0] is None else fields[0][:-1]

        topic_name = fields[1]

        year = int(fields[2])
        month = int(fields[3])
        day = int(fields[4])

        hour = int(fields[5])
        minute = int(fields[6])
        second = int(fields[7])

        created_datetime = dt(year, month, day, hour, minute, second, 0, pytz.UTC)

        return cls(created_datetime, topic_name, tag, file)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, created_datetime, topic_name, tag, file: File):
        """
        Constructor
        """
        self.__created_datetime = created_datetime          # datetime (offset-aware to UTC)
        self.__topic_name = topic_name                      # string
        self.__tag = tag                                    # string

        self.__file = file                                  # File


    # ----------------------------------------------------------------------------------------------------------------

    def path(self):
        return self.__file.path()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def created_datetime(self):
        return self.__created_datetime


    @property
    def topic_name(self):
        return self.__topic_name


    @property
    def tag(self):
        return self.__tag


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogFile:{created_datetime:%s, tag:%s, topic_name:%s, file:%s}" % \
               (self.created_datetime, self.tag, self.topic_name, self.__file)
