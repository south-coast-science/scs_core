"""
Created on 31 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A helper class for validating and preparing GPS module output strings.

https://www.nmea.org
https://en.wikipedia.org/wiki/NMEA_0183
"""


# --------------------------------------------------------------------------------------------------------------------

class NMEAReport(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def checksum(cls, text):
        cs = 0
        for c in text[1:]:
            cs ^= ord(c)

        return cs


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, line):
        main = line.strip().split("*")

        if len(main) != 2:
            raise ValueError("malformed line:%s" % (line.strip()))

        fields = [item.strip() for item in main[0].split(",")]
        cs = int(main[1], 16)

        if cs != cls.checksum(main[0]):
            raise ValueError("invalid checksum:%s" % (line.strip()))

        return NMEAReport(fields)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, fields):
        """
        Constructor
        """
        self.__fields = fields


    def __len__(self):
        return len(self.__fields)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def message_id(self):
        return self.str(0) if len(self) > 0 else None


    # ----------------------------------------------------------------------------------------------------------------

    def int(self, index):
        number_str = self.str(index)
        number = None if number_str is None else int(number_str)

        return number


    def float(self, index, precision):
        index_str = self.str(index)
        number = None if index_str is None else float(index_str)

        if number is None:
            return None

        return round(number, precision)


    def str(self, index):
        return self.__fields[index] if len(self.__fields[index]) > 0 else None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NMEAReport:{fields:%s}" % self.__fields
