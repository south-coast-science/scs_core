"""
Created on 31 Jan 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class NMEASentence(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, message_id):
        """
        Constructor
        """
        self.__message_id = message_id


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def message_id(self):
        return self.__message_id


    @property
    def source(self):
        return self.__message_id[2:3]
