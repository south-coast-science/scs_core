'''
Created on 24 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

from datetime import date


# --------------------------------------------------------------------------------------------------------------------

class Datum(object):
    '''
    classdocs
    '''
    
    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def float(number, ndigits):
        if number is None:
            return None

        try:
            value = float(number)
        except ValueError:
            return None

        return round(value, ndigits)


    @staticmethod
    def int(number):
        if number is None:
            return None

        try:
            value = float(number)
        except ValueError:
            return None

        return int(value)


    @staticmethod
    def date(isodate):
        if isodate is None:
            return None

        parts = isodate.split("-")

        if len(parts) != 3:
            return None

        try:
            year = int(float(parts[0]))
            month = int(float(parts[1]))
            day = int(float(parts[2]))
        except ValueError:
            return None

        return date(year, month, day)
