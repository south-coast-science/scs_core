"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION User defined exceptions for the aws_group_setup script
"""


# --------------------------------------------------------------------------------------------------------------------

class Error(Exception):
    """Base class for other exceptions"""
    pass


class ProjectMissingError(Error):
    """Raised when the project read fails"""
    pass
