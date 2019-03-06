"""
Created on 25 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import struct


# --------------------------------------------------------------------------------------------------------------------

class EEPROMImage(object):
    """
    Load a .eep file
    """
    @classmethod
    def construct_from_file(cls, filename, min_size=0):
        content = []

        # file content...
        f = open(filename, "rb")

        try:
            while True:
                byte = f.read(1)

                if not byte:
                    break

                content.append(struct.unpack('B', byte)[0])

        except RuntimeError:
            return None

        finally:
            f.close()

        # padding...
        if min_size and len(content) < min_size:
            content += [0] * (min_size - len(content))

        return EEPROMImage(content)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, content):
        """
        Constructor
        """
        self.__content = content


    def __len__(self):
        return len(self.__content)


    def __eq__(self, other):
        try:
            return self.content == other.content

        except AttributeError:
            return False


    def __ne__(self, other):
        return not self.__eq__(other)


    # ----------------------------------------------------------------------------------------------------------------

    def formatted(self, width):
        addr = 0

        while addr < len(self.__content):
            values = self.__content[addr: addr + width]

            hexs = ' '.join("%02x" % value for value in values)
            hexs = hexs.ljust(width * 3)

            chrs = ''.join(chr(value) if 31 < value < 128 else '.' for value in values)    # non-printable chars are '.'

            print("0x%04x: %s        %s" % (addr, hexs, chrs))

            addr += width


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def content(self):
        return self.__content


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "EEPROMImage:{content:%s}" % self.content
