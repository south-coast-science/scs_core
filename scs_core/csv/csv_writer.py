'''
Created on 2 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

import json
import sys
import _csv

from collections import OrderedDict

from scs_core.csv.csv_dict import CSVDict
from scs_core.csv.csv_logger import CSVLogger


# TODO: parameterise use of CSVLogger - don't use on big file!

# --------------------------------------------------------------------------------------------------------------------

class CSVWriter(object):
    '''
    classdocs
    '''

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filename = None):
        '''
        Constructor
        '''
        self.__filename = filename
        self.__has_header = False

        if self.__filename is None:
            self.__file = sys.stdout
            self.__writer = _csv.writer(self.__file)
        else:
            self.__file = open(self.__filename, "w")
            self.__writer = CSVLogger(self.__file)


    # ----------------------------------------------------------------------------------------------------------------

    def write(self, jstr):
        if not jstr:
            return

        jdict = json.loads(jstr, object_pairs_hook=OrderedDict)
        datum = CSVDict(jdict)

        if not self.__has_header:
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
    def has_header(self):
        return self.__has_header


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVWriter:{filename:%s, has_header:%s}" % (self.filename, self.has_header)
