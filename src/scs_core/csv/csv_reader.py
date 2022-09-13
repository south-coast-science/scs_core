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

    __REPRESENTATIONS_OF_NULL = ('', 'NULL')

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def list_dialects():
        return csv.list_dialects()


    @staticmethod
    def __recast(value):
        if value is None:
            return None

        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            pass

        if value.upper() == 'TRUE':
            return True

        if value.upper() == 'FALSE':
            return False

        return value


    @classmethod
    def __renullify(cls, value):
        try:
            return None if value.upper() in cls.__REPRESENTATIONS_OF_NULL else value
        except AttributeError:
            return value


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_for_file(cls, filename, cast=True, nullify=False, start_row=0):
        iterable = sys.stdin if filename is None else open(filename, "r")

        return cls(iterable, filename=filename, cast=cast, nullify=nullify,
                   start_row=start_row)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, iterable, filename=None, cast=True, nullify=False, start_row=0):
        """
        Constructor
        """
        self.__iterable = iterable                                  # iterable
        self.__filename = filename                                  # string
        self.__cast = bool(cast)                                    # bool
        self.__nullify = bool(nullify)                              # bool
        self.__start_row = int(start_row)                           # int

        try:
            self.__reader = csv.reader(iterable, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL,
                                       skipinitialspace=True)

            try:
                paths = next(self.__reader)
            except StopIteration:                                       # no input
                paths = []

            self.__read_count = 0                                       # int

            self.__header = CSVHeader.construct_from_paths(paths)       # CSVHeader

        except csv.Error as ex:
            raise CSVReaderException(ex)


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

                if self.__nullify:
                    row = (self.__renullify(cell) for cell in row)

                if self.__cast:
                    row = (self.__recast(cell) for cell in row)

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

        return "CSVReader:{iterable:%s, filename:%s, cast:%s, nullify:%s, " \
               "start_row:%s, read_count:%s, header:%s}" % \
               (iterable, self.filename, self.__cast, self.__nullify,
                self.__start_row, self.read_count, Str.collection(list(self.header.paths())))


# --------------------------------------------------------------------------------------------------------------------

class CSVReaderException(RuntimeError):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *args):
        super().__init__(*args)
