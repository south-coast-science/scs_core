"""
Created on 12 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class CSVLog(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def directory_name(cls, datetime):
        if datetime is None:
            raise ValueError("datetime may not be None")

        return "%04d-%02d" % (datetime.year, datetime.month)


    @classmethod
    def file_name(cls, datetime, topic, tag=None):
        if datetime is None:
            raise ValueError("datetime may not be None")

        if tag is None:
            return "%s-%4d-%02d-%02d-%02d-%02d-%02d.csv" % \
                   (topic, datetime.year, datetime.month, datetime.day,
                    datetime.hour, datetime.minute, datetime.second)

        return "%s-%s-%4d-%02d-%02d-%02d-%02d-%02d.csv" % \
               (tag, topic, datetime.year, datetime.month, datetime.day,
                datetime.hour, datetime.minute, datetime.second)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, root_path, topic, tag=None):
        """
        Constructor
        """
        self.__root_path = root_path                        # string
        self.__topic = topic                                # string
        self.__tag = tag                                    # string

        self.__timeline_start = None                        # datetime


    # ----------------------------------------------------------------------------------------------------------------

    def mkdir(self):
        Filesystem.mkdir(os.path.join(self.root_path, self.directory_name(self.timeline_start)))


    def directory_path(self):
        return os.path.join(self.root_path, self.directory_name(self.timeline_start))


    def file_path(self):
        return os.path.join(self.directory_path(), self.file_name(self.timeline_start, self.topic, self.tag))


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
    def topic(self):
        return self.__topic


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
        return "CSVLog:{root_path:%s, tag:%s, topic:%s, timeline_start:%s}" % \
               (self.root_path, self.tag, self.topic, self.timeline_start)
