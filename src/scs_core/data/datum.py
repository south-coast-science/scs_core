"""
Created on 24 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.python.org/3/library/struct.html
https://stackoverflow.com/questions/8022530/how-to-check-for-valid-email-address
"""

import math
import re
import struct

from datetime import date
from urllib.parse import urlparse


# --------------------------------------------------------------------------------------------------------------------

class Datum(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    # formatting...

    @classmethod
    def format(cls, value, leading_zeroes=False):
        # string or bool...
        if not cls.is_numeric(value):
            return "%s"

        # numeric...
        prefix = "0" if leading_zeroes else ""
        length = str(len((str(value))))

        if cls.is_int(value):
            return "%" + prefix + length + "d"

        # float...
        precision = str(cls.precision(value))

        return "%" + prefix + length + "." + precision + "f"


    @classmethod
    def is_email_address(cls, value):
        try:
            return bool(re.match(r'[^@\s]+@[^@\s]+\.[^@\s]+', value))
        except TypeError:
            return False


    @classmethod
    def is_url(cls, value):
        try:
            result = urlparse(value)
            return all((result.scheme, result.netloc))
        except AttributeError:
            return False


    @classmethod
    def is_true(cls, value):
        return value in ['True', 'true']


    # ----------------------------------------------------------------------------------------------------------------
    # morphological numeracy...

    @classmethod
    def is_numeric(cls, value):
        return cls.precision(value) is not None


    @classmethod
    def is_int(cls, value):
        precision = cls.precision(value)

        if precision is None:
            return False

        return precision == 0


    @classmethod
    def is_float(cls, value):
        precision = cls.precision(value)

        if precision is None:
            return False

        return precision > 0


    @staticmethod
    def precision(value):
        if value is None:
            return None

        if isinstance(value, bool):
            return None

        try:
            float(value)
        except ValueError:
            return None

        pieces = str(value).split('.')

        # int...
        if len(pieces) == 1:
            return 0                            # warning: round(123, 0) returns 123.0 - use round(123)

        # float...
        return len(pieces[1])                   # warning: interprets 1. as precision 0


    # ----------------------------------------------------------------------------------------------------------------
    # cast or None...

    @staticmethod
    def bool(field, default=None):
        if field is None:
            return default

        try:
            value = bool(field)
        except ValueError:
            return default

        return value


    @staticmethod
    def int(number, default=None):
        if number is None:
            return default

        try:
            value = int(float(number))              # because int('123.000') raises ValueError!!
        except ValueError:
            return default

        return value


    @staticmethod
    def float(number, ndigits=None, default=None):
        if number is None:
            return default

        try:
            value = float(number)
        except ValueError:
            return default

        return value if ndigits is None else round(value, ndigits)      # warning: round(123, 0) returns 123.0


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


# --------------------------------------------------------------------------------------------------------------------

class Encode(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    # encode byte array...

    @staticmethod
    def bool(value):
        return 1 if value else 0


    @staticmethod
    def int(value, order):
        unpacked = struct.unpack('BB', struct.pack(order + 'h', int(value)))

        return unpacked


    @staticmethod
    def unsigned_int(value, order):
        unpacked = struct.unpack('BB', struct.pack(order + 'H', int(value)))

        return unpacked


    @staticmethod
    def unsigned_long(value, order):
        unpacked = struct.unpack('BBBB', struct.pack(order + 'L', int(value)))

        return unpacked


    @staticmethod
    def float(value, order):
        unpacked = struct.unpack('BBBB', struct.pack(order + 'f', float(value)))

        return unpacked


# --------------------------------------------------------------------------------------------------------------------

class Decode(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    # decode byte array...

    @staticmethod
    def int(byte_values, order):
        packed = struct.unpack(order + 'h', struct.pack('BB', *byte_values))

        return packed[0]


    @staticmethod
    def unsigned_int(byte_values, order):
        packed = struct.unpack(order + 'H', struct.pack('BB', *byte_values))

        return packed[0]


    @staticmethod
    def long(byte_values, order):
        packed = struct.unpack(order + 'l', struct.pack('BBBB', *byte_values))

        return packed[0]


    @staticmethod
    def unsigned_long(byte_values, order):
        packed = struct.unpack(order + 'L', struct.pack('BBBB', *byte_values))

        return packed[0]


    @staticmethod
    def float(byte_values, order):
        packed = struct.unpack(order + 'f', struct.pack('BBBB', *byte_values))

        return None if math.isnan(packed[0]) else packed[0]


    @staticmethod
    def double(byte_values, order):
        packed = struct.unpack(order + 'd', struct.pack('BBBBBBBB', *byte_values))

        return None if math.isnan(packed[0]) else packed[0]
