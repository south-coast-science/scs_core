"""
Created on 4 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/43717757/commas-and-double-quotes-in-csv-files
"""

import csv
import _csv
import sys

from scs_core.csv.csv_dict import CSVHeader

from scs_core.data.json import JSONify


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


    @staticmethod
    def __nullify(value):
        return None if value == "" else value


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filename=None, numeric_cast=True, empty_string_as_null=False):
        """
        Constructor
        """
        self.__filename = filename                                          # string
        self.__file = sys.stdin if self.__filename is None else open(self.__filename, "r")

        self.__reader = csv.reader(self.__file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL,
                                   skipinitialspace=True)

        try:
            paths = next(self.__reader)
        except StopIteration:                   # no input
            paths = []

        self.__header = CSVHeader.construct_from_paths(paths)               # CSVHeader

        self.__numeric_cast = numeric_cast                                  # bool
        self.__empty_string_as_null = empty_string_as_null                  # bool


    # ----------------------------------------------------------------------------------------------------------------

    def close(self):
        if self.__filename is None:
            return

        self.__file.close()


    # ----------------------------------------------------------------------------------------------------------------

    def rows(self):
        try:
            for row in self.__reader:
                if len(row) == 0:
                    continue

                if self.__numeric_cast:
                    row = [self.__recast(cell) for cell in row]

                if self.__empty_string_as_null:
                    row = [self.__nullify(cell) for cell in row]

                datum = self.__header.as_dict([cell for cell in row])

                yield JSONify.dumps(datum)

        except _csv.Error as ex:
            raise CSVReaderException(ex)            # typically caused by a badly-closed CSV file


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def filename(self):
        return self.__filename


    @property
    def header(self):
        return self.__header


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        header = '[' + ', '.join(self.header.paths()) + ']'

        return "CSVReader:{filename:%s, numeric_cast:%s, empty_string_as_null:%s, header:%s}" % \
               (self.filename, self.__numeric_cast, self.__empty_string_as_null, header)


# --------------------------------------------------------------------------------------------------------------------

class CSVReaderException(Exception):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *args):
        super().__init__(*args)
