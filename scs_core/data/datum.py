"""
Created on 24 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from datetime import date

from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class Datum(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def bool(field):
        if field is None:
            return None

        try:
            value = bool(field)
        except ValueError:
            return None

        return value


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
    def date(iso_date):
        if iso_date is None:
            return None

        parts = iso_date.split("-")

        if len(parts) != 3:
            return None

        try:
            year = int(float(parts[0]))
            month = int(float(parts[1]))
            day = int(float(parts[2]))
        except ValueError:
            return None

        return date(year, month, day)


    @staticmethod
    def datetime(iso_datetime):
        if iso_datetime is None:
            return None

        try:
            value = LocalizedDatetime.construct_from_iso8601(iso_datetime)
        except ValueError:
            return None

        return value
