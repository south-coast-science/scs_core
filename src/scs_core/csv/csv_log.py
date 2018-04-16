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

    def __init__(self, root_path, device_tag, topic):
        """
        Constructor
        """
        self.__root_path = root_path                                # string
        self.__device_tag = device_tag                              # string
        self.__topic = topic                                        # string

        self.__timeline_start = None                                # datetime


    # ----------------------------------------------------------------------------------------------------------------

    def mkdir(self):
        Filesystem.mkdir(os.path.join(self.root_path, self.directory_name()))


    def directory_path(self):
        return os.path.join(self.root_path, self.directory_name())


    def file_path(self):
        return os.path.join(self.directory_path(), self.file_name())


    def directory_name(self):
        if self.timeline_start is None:
            raise ValueError("timeline_start has not been set")

        return "%04d-%02d" % (self.timeline_start.year, self.timeline_start.month)


    def file_name(self):
        if self.timeline_start is None:
            raise ValueError("timeline_start has not been set")

        return "%s-%4d-%02d-%02d-%02d-%02d-%02d-%s.csv" % \
               (self.device_tag,
                self.timeline_start.year, self.timeline_start.month, self.timeline_start.day,
                self.timeline_start.hour, self.timeline_start.minute, self.timeline_start.second,
                self.topic)


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
    def device_tag(self):
        return self.__device_tag


    @property
    def topic(self):
        return self.__topic


    @property
    def timeline_start(self):
        return self.__timeline_start


    @timeline_start.setter
    def timeline_start(self, localised_timeline_start):
        self.__timeline_start = localised_timeline_start.utc_datetime


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLog:{root_path:%s, device_tag:%s, topic:%s, timeline_start:%s}" % \
               (self.root_path, self.device_tag, self.topic, self.timeline_start)
