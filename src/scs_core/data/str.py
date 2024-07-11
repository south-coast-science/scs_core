"""
Created on 8 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class Str(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def bin16(value, separator=' '):
        formatted = ''

        for shift in (12, 8, 4, 0):
            nibble = (value >> shift) & 0x000f
            nibble_str = "{0:b}".format(nibble).rjust(4, '0')

            formatted += nibble_str + separator

        return formatted.strip(separator)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def collection(cls, value):
        if isinstance(value, list):
            return '[' + ', '.join(cls.collection(item) for item in value) + ']'

        if isinstance(value, tuple):
            return '(' + ', '.join(cls.collection(item) for item in value) + ')'

        try:
            return '{' + ', '.join(str(key) + ': ' + cls.collection(value[key]) for key in value) + '}'

        except TypeError:
            return str(value)
