"""
Created on 4 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import csv
import sys

from scs_core.csv.csv_dict import CSVHeader
from scs_core.data.json import JSONify


# TODO: deal with comma-terminated line dialect

# --------------------------------------------------------------------------------------------------------------------

class CSVReader(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def list_dialects():
        return csv.list_dialects()


    @staticmethod
    def __recast(value):
        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        return value


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filename=None):
        """
        Constructor
        """
        self.__filename = filename
        self.__file = sys.stdin if self.__filename is None else open(self.__filename, "r")

        self.__reader = csv.reader(self.__file)

        try:
            paths = next(self.__reader)
        except StopIteration:                   # no input
            paths = []

        self.__header = CSVHeader.construct_from_paths(paths)


    # ----------------------------------------------------------------------------------------------------------------

    def close(self):
        if self.__filename is None:
            return

        self.__file.close()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rows(self):
        for row in self.__reader:
            if len(row) == 0:
                continue

            datum = self.__header.as_dict([CSVReader.__recast(cell) for cell in row])

            yield JSONify.dumps(datum)


    @property
    def filename(self):
        return self.__filename


    @property
    def header(self):
        return self.__header


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        header = '[' + ', '.join(self.header.paths()) + ']'

        return "CSVReader:{filename:%s, header:%s}" % (self.filename, header)
