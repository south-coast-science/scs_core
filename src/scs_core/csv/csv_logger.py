"""
Created on 16 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import csv
import json

from collections import OrderedDict

from scs_core.csv.csv_dict import CSVDict

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class CSVLogger(object):
    """
    classdocs
    """

    MIN_FREE_SPACE = 1048576            # 1MB

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

        # first run...
        if not self.__file:
            self.__open_file()

        # start log for new day...
        if not self.log.in_timeline(LocalizedDatetime.now()):
            self.close()
            self.__open_file()

        # write header...
        if not self.__header:
            self.__header = datum.header
            self.__writer.writerow(self.__header)

        # write row...
        self.__writer.writerow(datum.row)
        self.__file.flush()


    def close(self):
        if self.__file is None:
            return

        self.__file.close()
        self.__file = None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def log(self):
        return self.__log


    # ----------------------------------------------------------------------------------------------------------------

    def __open_file(self):
        self.log.timeline_start = LocalizedDatetime.now()

        self.__clear_space()
        self.log.mkdir()

        self.__file = open(self.log.file_path(), "w")
        self.__writer = csv.writer(self.__file, quoting=csv.QUOTE_MINIMAL)

        if self.__header:
            self.__writer.writerow(self.__header)


    def __clear_space(self):                    # TODO: check disk usage
        while self.__delete_oldest():
            continue


    def __delete_oldest(self):
        containers = Filesystem.ls(self.log.root_path)

        for container in containers:
            if not container.is_directory:
                continue

            files = Filesystem.ls(container.path())

            for file in files:
                if not file.is_directory and file.has_suffix('csv'):
                    success = file.delete()
                    Filesystem.rmdir(container.path())          # remove empty directories

                    return success

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogger:{log:%s}" % self.log
