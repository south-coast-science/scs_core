"""
Created on 19 May 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class NetworkUnavailableException(RuntimeError):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, ex):
        return cls(ex.__class__.__name__, str(ex))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, original_exception_classname, original_message,  *args):
        super().__init__(*args)

        self.__original_exception_classname = original_exception_classname
        self.__original_message = original_message


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return ': '.join((self.__original_exception_classname, self.__original_message))
