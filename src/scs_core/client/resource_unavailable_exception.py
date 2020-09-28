"""
Created on 19 May 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class ResourceUnavailableException(RuntimeError):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, url, original_exception, *args, **kwargs):
        super().__init__(args, kwargs)

        self.__url = url                                                # string
        self.__original_exception = original_exception                  # Exception


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def url(self):
        return self.__url


    @property
    def original_exception(self):
        return self.__original_exception


    # ----------------------------------------------------------------------------------------------------------------

    def __repr__(self):
        return "%s: %s: %s" % \
               (self.url, self.original_exception.__class__.__name__, str(self.original_exception))


    def __str__(self, *args, **kwargs):
        return "ResourceUnavailableException:{url:%s, original_exception:%s}" % \
               (self.url, str(self.original_exception))
