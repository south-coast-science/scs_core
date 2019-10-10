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


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filename=None, cast=True):
        """
        Constructor
        """
        self.__filename = filename
        self.__file = sys.stdin if self.__filename is None else open(self.__filename, "r")

        self.__reader = csv.reader(self.__file, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL,
                                   skipinitialspace=True)

        try:
            paths = next(self.__reader)
        except StopIteration:                   # no input
            paths = []

        self.__header = CSVHeader.construct_from_paths(paths)

        self.__cast = cast


    # ----------------------------------------------------------------------------------------------------------------

    def close(self):
        if self.__filename is None:
            return

        self.__file.close()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rows(self):
        try:
            for row in self.__reader:
                if len(row) == 0:
                    continue

                if self.__cast:
                    datum = self.__header.as_dict([CSVReader.__recast(cell) for cell in row])

                else:
                    datum = self.__header.as_dict([cell for cell in row])

                yield JSONify.dumps(datum)

        except _csv.Error as ex:
            raise CSVReaderException(ex)            # typically caused by a badly-closed CSV file


    @property
    def filename(self):
        return self.__filename


    @property
    def header(self):
        return self.__header


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        header = '[' + ', '.join(self.header.paths()) + ']'

        return "CSVReader:{filename:%s, cast:%s, header:%s}" % (self.filename, self.__cast, header)


# --------------------------------------------------------------------------------------------------------------------

class CSVReaderException(Exception):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *args):
        super().__init__(*args)
