"""
Created on 21 Dec 2020

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION User defined exceptions for dynamo message manager because no BOTO
"""


# --------------------------------------------------------------------------------------------------------------------

class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidKeyError(Error):
    """Raised when the project read fails"""
    pass
