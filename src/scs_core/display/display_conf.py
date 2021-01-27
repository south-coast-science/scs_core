"""
Created on 27 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

a stub display configuration, to be implemented elsewhere
"""


# --------------------------------------------------------------------------------------------------------------------

class DisplayConf(object):
    """
    classdocs
    """

    @classmethod
    def modes(cls):
        return []


    @classmethod
    def load(cls, manager, encryption_key=None):
        raise NotImplementedError


    @classmethod
    def delete(cls, manager):
        raise NotImplementedError


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, _mode, _device_name, _startup_message, _shutdown_message, _show_time):
        """
        Constructor
        """
        raise NotImplementedError


    def save(self, manager, encryption_key=None):
        raise NotImplementedError
