"""
Created on 2 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import csv
import json
import os
import sys

from collections import OrderedDict

from scs_core.csv.csv_dict import CSVDict


# TODO: why use _csv?
# TODO: batch mode - where all rows are scanned for header fields and the data not released until input is complete

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
        self.__has_header = False

        if self.__filename is None:
            self.__append = append

            self.__file = sys.stdout
            self.__writer = csv.writer(self.__file)
        else:
            self.__append = append and os.path.exists(self.__filename)

            self.__file = open(self.__filename, "a" if self.__append else "w")
            self.__writer = csv.writer(self.__file, quoting=csv.QUOTE_MINIMAL)


    # ----------------------------------------------------------------------------------------------------------------

    def write(self, jstr):
        if not jstr:
            return

        jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
        datum = CSVDict(jdict)

        if not self.__has_header and not self.__append:
            self.__writer.writerow(datum.header)
            self.__has_header = True

        self.__writer.writerow(datum.row)
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
        return "CSVWriter:{filename:%s, append:%s}" % (self.filename, self.__append)
