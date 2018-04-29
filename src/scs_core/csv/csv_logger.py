"""
Created on 16 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import csv
import json
import sys
import time

from collections import OrderedDict

from scs_core.csv.csv_dict import CSVDict

from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class CSVLogger(object):
    """
    classdocs
    """

    __MIN_FREE_SPACE = 10485760                 # 10MB

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, host, log, delete_oldest, write_interval):
        """
        Constructor
        """
        self.__host = host                              # Host
        self.__log = log                                # CSVLog
        self.__delete_oldest = delete_oldest            # bool
        self.__write_interval = write_interval          # int

        self.__header = None                            # array of string
        self.__file = None                              # file handle
        self.__latest_write = None                      # timestamp
        self.__writing_inhibited = False                # bool

        self.__buffer = []                              # array of CSVDict


    # ----------------------------------------------------------------------------------------------------------------

    def write(self, jstr):
        if self.writing_inhibited:
            return

        if jstr is None or self.log is None:
            return

        jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
        datum = CSVDict(jdict)

        # direct write...
        if not self.write_interval:
            self.__write(datum)
            return

        # interval write...
        now = int(round(time.time()))

        if self.__latest_write is None:
            self.__latest_write = now

        # append to buffer...
        if (now - self.__latest_write) < self.write_interval:
            self.__buffer.append(datum)
            return

        self.__latest_write = now

        # flush buffer...
        for datum in self.__buffer:
            self.__write(datum)

        self.__buffer = []


    def close(self):
        if self.__file is None:
            return

        self.__file.close()
        self.__file = None


    # ----------------------------------------------------------------------------------------------------------------

    def __write(self, datum):
        # first run...
        if not self.__file:
            if self.log.tag is None and 'tag' in datum.dictionary:
                self.log.tag = datum.dictionary['tag']                  # find the tag from the first document

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


    def __open_file(self):
        self.log.timeline_start = LocalizedDatetime.now()

        self.__clear_space()
        self.log.mkdir()

        self.__file = open(self.log.file_path(), "w")
        self.__writer = csv.writer(self.__file, quoting=csv.QUOTE_MINIMAL)

        if self.__header:
            self.__writer.writerow(self.__header)


    def __clear_space(self):
        if self.__has_sufficient_space():
            return

        # stop on no-delete...
        if not self.delete_oldest:
            print("CSVLogger.__clear_space: volume full.", file=sys.stderr)
            self.__writing_inhibited = True
            return

        # delete until enough free...
        while not self.__has_sufficient_space():
            success = self.__delete_oldest_log()

            if not success:
                print("CSVLogger.__clear_space: delete failed.", file=sys.stderr)
                self.__writing_inhibited = True
                return


    def __has_sufficient_space(self):
        du = self.__host.disk_usage(self.log.root_path)
        print("CSVLogger.__has_sufficient_space: du: %s" % du, file=sys.stderr)

        return du.free > self.__MIN_FREE_SPACE


    def __delete_oldest_log(self):
        # walk the directories...
        containers = Filesystem.ls(self.log.root_path)

        for container in containers:
            if not container.is_directory:
                continue

            # walk the files...
            files = Filesystem.ls(container.path())

            for file in files:
                if not file.is_directory and file.has_suffix('csv'):
                    print("CSVLogger.__delete_oldest_log: deleting: %s" % file, file=sys.stderr)

                    success = file.delete()

                    if not success:
                        return False

                    Filesystem.rmdir(container.path())          # remove empty directories

                    return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def log(self):
        return self.__log


    @property
    def delete_oldest(self):
        return self.__delete_oldest


    @property
    def write_interval(self):
        return self.__write_interval


    @property
    def writing_inhibited(self):
        return self.__writing_inhibited


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogger:{log:%s, delete_oldest:%s, write_interval:%s, writing_inhibited:%s}" % \
               (self.log, self.delete_oldest, self.write_interval, self.writing_inhibited)
