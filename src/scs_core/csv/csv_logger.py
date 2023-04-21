"""
Created on 16 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import csv
import time

from scs_core.csv.csv_dict import CSVDict

from scs_core.data.datetime import LocalizedDatetime

from scs_core.sys.filesystem import Filesystem
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class CSVLogger(object):
    """
    classdocs
    """

    __MIN_FREE_SPACE = 10485760                         # 10MB
    __CHECK_INTERVAL = 4                                # normally once per day


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, host, log, delete_oldest, write_interval):
        manager = CSVSpaceManager(host, log, delete_oldest, cls.__MIN_FREE_SPACE, cls.__CHECK_INTERVAL)

        return cls(host, log, manager, write_interval)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, log, manager, write_interval):
        """
        Constructor
        """
        self.__host = host                              # PersistenceManager
        self.__log = log                                # CSVLog
        self.__manager = manager                        # CSVSpaceManager
        self.__write_interval = write_interval          # int

        self.__paths = None                             # array of string
        self.__file = None                              # file handle
        self.__latest_write = None                      # timestamp
        self.__writing_inhibited = False                # bool

        self.__buffer = []                              # array of CSVDict


    # ----------------------------------------------------------------------------------------------------------------

    def write(self, jstr):
        if self.writing_inhibited:
            return None

        if jstr is None or self.log is None:
            return None

        datum = CSVDict.construct_from_jstr(jstr)

        if datum is None:
            return None

        # direct write...
        if not self.write_interval:
            self.__write(datum)
            self.__file.flush()
            return self.log.file_path()

        # interval write...
        now = time.time()

        if self.__latest_write is None:
            self.__latest_write = now

        interval = now - self.__latest_write

        # append to buffer...
        if interval < self.write_interval:
            self.__buffer.append(datum)
            return self.log.file_path()

        self.__latest_write = now

        # deferred write...
        for datum in self.__buffer:
            self.__write(datum)

        self.__file.flush()

        self.__buffer = []

        return self.log.file_path()


    def close(self):
        if self.__file is None:
            return

        self.__file.close()
        self.__file = None


    # ----------------------------------------------------------------------------------------------------------------

    def __write(self, datum):
        # first run...
        if not self.__file:
            if self.log.tag is None and 'tag' in datum.collection:
                self.log.tag = datum.collection['tag']

            self.__open_file()

        # start log for new day...
        if not self.log.in_timeline(LocalizedDatetime.now().utc()):
            self.close()
            self.__open_file()

        # write header...
        if not self.__paths:
            self.__paths = datum.paths()
            self.__writer.writerow(self.__paths)

        # write row...
        self.__writer.writerow(datum.row(self.__paths))


    def __open_file(self):
        self.log.timeline_start = LocalizedDatetime.now().utc()

        # check...
        if not self.__manager.clear_space():
            self.writing_inhibited = True

        self.log.mkdir()

        # file...
        self.__file = open(self.log.file_path(), "w")
        self.__writer = csv.writer(self.__file, quoting=csv.QUOTE_MINIMAL)

        # header...
        if self.__paths:
            self.__writer.writerow(self.__paths)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def log(self):
        return self.__log


    @property
    def write_interval(self):
        return self.__write_interval


    @property
    def writing_inhibited(self):
        return self.__writing_inhibited


    @writing_inhibited.setter
    def writing_inhibited(self, writing_inhibited):
        self.__writing_inhibited = writing_inhibited


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogger:{log:%s, manager:%s, write_interval:%s, writing_inhibited:%s}" % \
               (self.log, self.__manager, self.write_interval, self.writing_inhibited)


# --------------------------------------------------------------------------------------------------------------------

class CSVSpaceManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, log, delete_oldest, min_free_space, check_interval):
        self.__logger = Logging.getLogger()

        self.__host = host                                          # PersistenceManager
        self.__log = log                                            # CSVLog
        self.__delete_oldest = delete_oldest                        # bool
        self.__min_free_space = min_free_space                      # int
        self.__check_interval = check_interval                      # int

        self.__check_count = check_interval


    # ----------------------------------------------------------------------------------------------------------------

    def clear_space(self):
        self.__check_count += 1

        if self.__check_count < self.__check_interval:
            return True

        self.__check_count = 0
        return self.__clear_space()


    # ----------------------------------------------------------------------------------------------------------------

    def __clear_space(self):
        if self.__has_sufficient_space():
            return True

        # stop on no-delete...
        if not self.__delete_oldest:
            self.__logger.error("CSVSpaceManager.__clear_space: volume full.")
            return False

        # delete until enough free...
        while not self.__has_sufficient_space():
            success = self.__delete_oldest_log()

            if not success:
                self.__logger.error("CSVSpaceManager.__clear_space: delete failed.")
                return False

        return True


    def __has_sufficient_space(self):
        du = self.__host.disk_usage(self.__log.root_path)

        return du.free > self.__min_free_space


    def __delete_oldest_log(self):
        # walk the directories...
        containers = Filesystem.ls(self.__log.root_path)

        for container in containers:
            if not container.is_directory:
                continue

            # walk the files...
            files = Filesystem.ls(container.path())

            for file in files:
                if not file.is_directory and file.has_suffix('csv'):
                    self.__logger.error("CSVSpaceManager.__delete_oldest_log: deleting: %s" % file)

                    success = file.delete()

                    if not success:
                        return False

                    Filesystem.rmdir(container.path())          # remove empty directories

                    return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVSpaceManager:{delete_oldest:%s, min_free_space:%s}" %  \
               (self.__delete_oldest, self.__min_free_space)
