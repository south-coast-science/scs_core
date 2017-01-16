"""
Created on 7 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
25 June 2016 17:44:28 BST: {"datum":{"conc":92,"dens":184},"measured-at":"2016-06-25T17:41:01+01:00"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MessageBody(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, data):
        """
        Constructor
        """
        self.__data = data                  # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['data'] = self.data

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def data(self):
        return self.__data


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MessageBody:{data:%s}" % self.data
