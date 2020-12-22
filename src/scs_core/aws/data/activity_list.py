"""
Created on 06 Nov 2020

@author: Jade Page (jade.page@southcoastscience.com)

"""

# Called activity_list because when it's renamed to status_list pycharm doesn't recognise it as a .py..

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class StatusList(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_status_list"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        status_list = jdict.get('status_list')

        return StatusList(status_list)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status_list):
        """
        Constructor
        """
        self.__status_list = status_list

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def status_list(self):
        return self.__status_list

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['status_list'] = self.__status_list

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "StatusList:{status_list:%s}" %  \
               self.__status_list
