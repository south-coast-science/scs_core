"""
Created on 15 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import socket


# --------------------------------------------------------------------------------------------------------------------

class AWS(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __REGION =            'us-west-2'

    @classmethod
    def region(cls):
        return cls.__REGION


    @classmethod
    def group_name(cls):
        host_name = socket.gethostname()
        return host_name + "-group"


    @classmethod
    def core_name(cls):
        host_name = socket.gethostname()
        return host_name + "-core"

