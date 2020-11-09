"""
Created on 4 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/43717757/commas-and-double-quotes-in-csv-files
"""

import csv
import sys

from scs_core.csv.csv_dict import CSVHeader

from scs_core.data.json import JSONify
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class CSVReader(object):
    """
    classdocs
    """

    __REPRESENTATIONS_OF_NULL = ('', 'null', 'NULL')

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


    @classmethod
    def __nullify(cls, value):
        return None if value in cls.__REPRESENTATIONS_OF_NULL else value


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_for_file(cls, filename, numeric_cast=True, empty_string_as_null=False, start_row=0):
        iterable = sys.stdin if filename is None else open(filename, "r")

        return cls(iterable, filename=filename, numeric_cast=numeric_cast, empty_string_as_null=empty_string_as_null,
                   start_row=start_row)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, iterable, filename=None, numeric_cast=True, empty_string_as_null=False, start_row=0):
        """
        Constructor
        """
        self.__iterable = iterable                                              # iterable
        self.__filename = filename                                              # string
        self.__numeric_cast = bool(numeric_cast)                                # bool
        self.__empty_string_as_null = bool(empty_string_as_null)                # bool
        self.__start_row = int(start_row)                                       # int

        self.__reader = csv.reader(iterable, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)

        try:
            paths = next(self.__reader)
        except StopIteration:                                                   # no input
            paths = []

        self.__read_count = 0                                                   # int

        self.__header = CSVHeader.construct_from_paths(paths)                   # CSVHeader


    # ----------------------------------------------------------------------------------------------------------------

    def close(self):
        if self.__filename is None:
            return

        self.__iterable.close()


    # ----------------------------------------------------------------------------------------------------------------

    def rows(self):
        row_number = -1

        try:
            for row in self.__reader:
                if len(row) == 0:
                    continue

                row_number += 1

                if row_number < self.__start_row:
                    continue

                if self.__numeric_cast:
                    row = [self.__recast(cell) for cell in row]

                if self.__empty_string_as_null:
                    row = [self.__nullify(cell) for cell in row]

                datum = self.__header.as_dict([cell for cell in row])

                yield JSONify.dumps(datum)

                self.__read_count += 1

        except csv.Error as ex:
            raise CSVReaderException(ex)            # typically on the last line of a badly-closed CSV file


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def filename(self):
        return self.__filename


    @property
    def read_count(self):
        return self.__read_count


    @property
    def header(self):
        return self.__header


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        iterable = self.__iterable.__class__.__name__

        return "CSVReader:{iterable:%s, filename:%s, numeric_cast:%s, empty_string_as_null:%s, " \
               "start_row:%s, read_count:%s, header:%s}" % \
               (iterable, self.filename, self.__numeric_cast, self.__empty_string_as_null,
                self.__start_row, self.read_count, Str.collection(list(self.header.paths())))


# --------------------------------------------------------------------------------------------------------------------

class CSVReaderException(RuntimeError):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *args):
        super().__init__(*args)
