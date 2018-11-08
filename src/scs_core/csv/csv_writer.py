"""
Created on 2 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import csv
import os
import sys

from scs_core.csv.csv_dict import CSVDict


# TODO: for an append, use the header in the existing file

# --------------------------------------------------------------------------------------------------------------------

class CSVWriter(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filename=None, append=False):
        """
        Constructor
        """
        self.__filename = filename
        self.__paths = None

        if self.__filename is None:
            self.__append = append

            self.__file = sys.stdout
            self.__writer = csv.writer(self.__file, quoting=csv.QUOTE_MINIMAL)
        else:
            self.__append = append and os.path.exists(self.__filename)

            self.__file = open(self.__filename, "a" if self.__append else "w")
            self.__writer = csv.writer(self.__file, quoting=csv.QUOTE_MINIMAL)


    # ----------------------------------------------------------------------------------------------------------------

    def write(self, jstr):
        if jstr is None:
            return

        datum = CSVDict.construct_from_jstr(jstr)

        if datum is None:
            return

        if self.__paths is None:
            self.__paths = datum.header.paths

            if not self.__append:
                self.__writer.writerow(self.__paths)

        self.__writer.writerow(datum.row(self.__paths))
        self.__file.flush()


    def close(self):
        if self.filename is None:
            return

        self.__file.close()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def filename(self):
        return self.__filename


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVWriter:{filename:%s, append:%s, paths:%s}" % (self.filename, self.__append, self.__paths)
