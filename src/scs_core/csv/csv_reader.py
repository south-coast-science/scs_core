"""
Created on 4 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import csv
import sys

from scs_core.csv.csv_dict import CSVDict
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class CSVReader(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

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
        self.__header = next(self.__reader)


    # ----------------------------------------------------------------------------------------------------------------

    def close(self):
        if self.__filename is None:
            return

        self.__file.close()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rows(self):
        for row in self.__reader:
            try:
                datum = CSVDict.as_dict(self.__header, [CSVReader.__recast(cell) for cell in row])
            except IndexError:                                                                          # TODO: fix!
                continue

            yield JSONify.dumps(datum)


    @property
    def filename(self):
        return self.__filename


    @property
    def header(self):
        return self.__header


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVReader:{filename:%s, header:%s}" % (self.filename, self.header)
