"""
Created on 2 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import _csv
import json
import os
import sys

from collections import OrderedDict

from scs_core.csv.csv_dict import CSVDict
from scs_core.csv.csv_logger import CSVLogger


# TODO: parameterise use of CSVLogger - don't use on big file!

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
            self.__append = False

            self.__file = sys.stdout
            self.__writer = _csv.writer(self.__file)
        else:
            self.__append = append and os.path.exists(self.__filename)

            self.__file = open(self.__filename, "a" if self.__append else "w")
            self.__writer = CSVLogger(self.__file)


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

        if self.__filename is None:
            sys.stdout.flush()


    def close(self):
        if self.__filename is None:
            return

        self.__writer.flush()
        self.__file.close()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def filename(self):
        return self.__filename


    @property
    def append(self):
        return self.__append


    @property
    def has_header(self):
        return self.__has_header


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVWriter:{filename:%s, append:%s, has_header:%s}" % (self.filename, self.append, self.has_header)
