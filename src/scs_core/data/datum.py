"""
Created on 24 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import math
import struct

from datetime import date

from scs_core.data.localized_datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class Datum(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------
    # encode byte array...

    @staticmethod
    def encode_int(value):
        unpacked = struct.unpack('BB', struct.pack('h', int(value)))

        return unpacked


    @staticmethod
    def encode_unsigned_int(value):
        unpacked = struct.unpack('BB', struct.pack('H', int(value)))

        return unpacked


    @staticmethod
    def encode_unsigned_long(value):
        unpacked = struct.unpack('BBBB', struct.pack('L', int(value)))

        return unpacked


    @staticmethod
    def encode_float(value):
        unpacked = struct.unpack('BBBB', struct.pack('f', float(value)))

        return unpacked


    # ----------------------------------------------------------------------------------------------------------------
    # decode byte array...

    @staticmethod
    def decode_int(byte_values):
        packed = struct.unpack('h', struct.pack('BB', *byte_values))
        return packed[0]


    @staticmethod
    def decode_unsigned_int(byte_values):
        packed = struct.unpack('H', struct.pack('BB', *byte_values))
        return packed[0]


    @staticmethod
    def decode_unsigned_long(byte_values):
        packed = struct.unpack('L', struct.pack('BBBB', *byte_values))
        return packed[0]


    @staticmethod
    def decode_float(byte_values):
        packed = struct.unpack('f', struct.pack('BBBB', *byte_values))

        return None if math.isnan(packed[0]) else packed[0]


    @staticmethod
    def decode_double(byte_values):
        packed = struct.unpack('d', struct.pack('BBBBBBBB', *byte_values))

        return None if math.isnan(packed[0]) else packed[0]


    # ----------------------------------------------------------------------------------------------------------------
    # cast or None...

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
