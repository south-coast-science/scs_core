'''
Created on 31 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://en.wikipedia.org/wiki/NMEA_0183
'''


# --------------------------------------------------------------------------------------------------------------------

class NMEASentence(object):
    '''
    classdocs
    '''

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

        return NMEASentence(fields)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, fields):
        '''
        Constructor
        '''
        self.__fields = fields


    def __len__(self):
        return len(self.__fields)


    # ----------------------------------------------------------------------------------------------------------------

    def int(self, index):
        str = self.str(index)
        number = None if str is None else int(str)

        return number


    def float(self, index, precision):
        str = self.str(index)
        number = None if str is None else float(str)

        if number is None:
            return None

        return round(number, precision)


    def str(self, index):
        return self.__fields[index] if len(self.__fields[index]) > 0 else None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NMEASentence:{fields:%s}" % self.__fields
