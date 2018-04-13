"""
Created on 12 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class CSVLog(object):

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, root_path, device_tag, subject, localised_timeline_start):
        """
        Constructor
        """
        self.__root_path = root_path
        self.__device_tag = device_tag
        self.__subject = subject

        timeline_start = localised_timeline_start.utc()

        self.__timeline_start = timeline_start.datetime


    # ----------------------------------------------------------------------------------------------------------------

    def in_timeline(self, localised_datetime):
        utc_localised_datetime = localised_datetime.utc()

        return utc_localised_datetime.datetime.date() == self.__timeline_start.date()


    def mkdir(self):
        Filesystem.mkdir(os.path.join(self.root_path, self.directory_name()))


    def abs_file_name(self):
        return os.path.join(self.root_path, self.directory_name(), self.file_name())


    def directory_name(self):
        return "%04d-%02d" % (self.timeline_start.year, self.timeline_start.month)


    def file_name(self):
        return "%sD%4d-%02d-%02dT%02d-%02d-%02dS%s.csv" % \
               (self.device_tag,
                self.timeline_start.year, self.timeline_start.month, self.timeline_start.day,
                self.timeline_start.hour, self.timeline_start.minute, self.timeline_start.second,
                self.subject)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def root_path(self):
        return self.__root_path


    @property
    def device_tag(self):
        return self.__device_tag


    @property
    def subject(self):
        return self.__subject


    @property
    def timeline_start(self):
        return self.__timeline_start


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLog:{root_path:%s, device_tag:%s, subject:%s, timeline_start:%s}" % \
               (self.root_path, self.device_tag, self.subject, self.timeline_start)
