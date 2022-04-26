"""
Created on 2 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class IPv4Address(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid(cls, dot_decimal):
        try:
            octets = [int(octet) for octet in dot_decimal.split('.') if 0 <= int(octet) <= 255]
        except (TypeError, ValueError):
            return False

        if len(octets) != 4:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, dot_decimal):
        if dot_decimal is None:
            return None

        octets = [int(octet) for octet in dot_decimal.split('.')]

        return cls(octets)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, octets):
        """
        Constructor
        """
        self.__octets = octets                          # array of int


    # ----------------------------------------------------------------------------------------------------------------

    def lso_range(self, start, end):
        if not 0 < start < 255:
            raise ValueError(start)

        if not 0 < end < 255:
            raise ValueError(end)

        for i in range(start, end + 1, 1):
            yield IPv4Address(self.__octets[:-1] + [i])


    # ----------------------------------------------------------------------------------------------------------------

    def dot_decimal(self):
        return '.'.join([str(octet) for octet in self.__octets])


    def __str__(self, *args, **kwargs):
        return "IPv4Address:{%s}" %  self.dot_decimal()

