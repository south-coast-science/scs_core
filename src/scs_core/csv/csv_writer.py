"""
Created on 2 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/3348460/csv-file-written-with-python-has-blank-lines-between-each-row
"""

import csv
import os
import sys

from scs_core.csv.csv_dict import CSVDict


# --------------------------------------------------------------------------------------------------------------------

class CSVWriter(object):
    """
    classdocs
    """

    QUOTING = csv.QUOTE_MINIMAL

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filename=None, append=False, exclude_header=False, header_scan=False):
        """
        Constructor
        """
        self.__filename = filename
        self.__paths = []

        if self.__filename is None:
            self.__append = append

            self.__file = sys.stdout
            self.__writer = csv.writer(self.__file, quoting=self.QUOTING)
        else:
            self.__append = append and os.path.exists(self.__filename)

            if self.__append and not header_scan:
                self.__paths = self.__append_paths()

            self.__file = open(self.__filename, "a" if self.__append else "w", newline='')
            self.__writer = csv.writer(self.__file, quoting=self.QUOTING)

        self.__exclude_header = exclude_header
        self.__header_scan = header_scan

        self.__data = []


    # ----------------------------------------------------------------------------------------------------------------

    def __append_paths(self):
        file = sys.stdin if self.__filename is None else open(self.__filename, "r")
        reader = csv.reader(file)

        paths = next(reader)

        file.close()

        return paths


    # ----------------------------------------------------------------------------------------------------------------

    def write(self, jstr):
        if jstr is None:
            return False

        datum = CSVDict.construct_from_jstr(jstr)

        if datum is None:
            return False

        if self.__header_scan:
            self.__data.append(datum)

            for path in datum.paths():
                if path not in self.__paths:
                    self.__paths.append(path)

            return True

        if not self.__paths:
            self.__paths = datum.paths()

            # write header...
            if not self.__append and not self.__exclude_header:
                self.__writer.writerow(self.__paths)

        # write row...
        self.__writer.writerow(datum.row(self.__paths))
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

    @property
    def filename(self):
        return self.__filename


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVWriter:{filename:%s, append:%s, exclude_header:%s, header_scan:%s, paths:%s}" % \
               (self.filename, self.__append, self.__exclude_header, self.__header_scan, self.__paths)
