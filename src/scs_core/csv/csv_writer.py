"""
Created on 2 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
"""

import csv
import os
import sys

from scs_core.csv.csv_dict import CSVDict
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class CSVWriter(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filename=None, append=False, exclude_header=False, header_scan=False, quote_all=False):
        """
        Constructor
        """
        self.__filename = filename
        self.__paths = []

        quoting = csv.QUOTE_ALL if quote_all else csv.QUOTE_MINIMAL

        if self.__filename is None:
            self.__append = append

            self.__file = sys.stdout
            self.__writer = csv.writer(self.__file, quoting=quoting)
        else:
            self.__append = append and os.path.exists(self.__filename)

            if self.__append and not header_scan:
                self.__paths = self.__build_paths()

            self.__file = open(self.__filename, "a" if self.__append else "w", newline='')
            self.__writer = csv.writer(self.__file, quoting=quoting)

        self.__exclude_header = exclude_header
        self.__header_scan = header_scan

        self.__data = []


    # ----------------------------------------------------------------------------------------------------------------

    def write(self, jstr):
        if jstr is None:
            return False

        datum = CSVDict.construct_from_jstr(jstr)

        if datum is None:
            return False

        if self.__header_scan:
            self.__data.append(datum)
            self.__update_paths(datum)

            return True

        if not self.__paths:
            self.__paths = datum.paths()

            # write header...
            if not self.__append and not self.__exclude_header:
                self.__writer.writerow(self.__paths)

        # write row...
        self.__writer.writerow(datum.row(self.__paths))

        if self.filename is None:
            self.__file.flush()

        return True


    def close(self):
        if self.__header_scan:
            # write header...
            self.__writer.writerow(self.__paths)

            # write rows...
            for datum in self.__data:
                self.__writer.writerow(datum.row(self.__paths))

        if self.filename is None:
            return

        self.__file.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __build_paths(self):
        file = sys.stdin if self.__filename is None else open(self.__filename, "r")
        reader = csv.reader(file)

        paths = next(reader)

        file.close()

        return paths


    def __update_paths(self, datum):
        datum_paths = datum.paths()

        appended_paths = []
        for i in range(len(datum_paths)):
            if datum_paths[i] not in self.__paths and not self.__is_sub_path(datum_paths[i], self.__paths):
                self.__paths.insert(i, datum_paths[i])
                appended_paths.append(datum_paths[i])

        if appended_paths:
            for i in reversed(range(len(self.__paths))):
                if self.__is_sub_path(self.__paths[i], appended_paths):
                    self.__paths.pop(i)


    @staticmethod
    def __is_sub_path(candidate, paths):
        for path in paths:
            if candidate == path:
                return False            # exit here because paths are assumed to be unique

            if PathDict.sub_path_includes_path(candidate, path):
                return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def filename(self):
        return self.__filename


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVWriter:{filename:%s, append:%s, exclude_header:%s, header_scan:%s, paths:%s}" % \
               (self.filename, self.__append, self.__exclude_header, self.__header_scan, self.__paths)
