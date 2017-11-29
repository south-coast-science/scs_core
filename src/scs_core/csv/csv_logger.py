"""
Created on 10 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from _csv import writer


# --------------------------------------------------------------------------------------------------------------------

class CSVLogger(object):
    """
    heap memory storage of CSV data
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, filename):
        self.__filename = filename
        self.__log = []


    # ----------------------------------------------------------------------------------------------------------------

    def writerow(self, row):
        self.__log.append(tuple(row))


    def flush(self):
        csv = writer(self.__filename)

        for row in self.__log:
            csv.writerow(row)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CSVLogger:{filename:%s, log:%s}" % (self.__filename, self.__log)
