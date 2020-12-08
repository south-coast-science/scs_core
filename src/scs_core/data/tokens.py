"""
Created on 8 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class Tokens(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, text, separator):
        if not text:
            return cls([])

        stripped_text = text.strip(separator)

        if not stripped_text:
            return cls([])

        return cls(stripped_text.split(separator))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tokens):
        """
        Constructor
        """
        self.__tokens = tokens                                # array of string


    def __len__(self):
        return len(self.tokens)


    def __eq__(self, other):
        return other.tokens == self.tokens


    # ----------------------------------------------------------------------------------------------------------------

    def startswith(self, other):
        if len(other) > len(self):
            return False

        for index in range(len(other)):
            if other.token(index) != self.token(index):
                return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def token(self, index):
        return self.__tokens[index]


    @property
    def tokens(self):
        return self.__tokens


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Tokens:{%s}" %  self.tokens
