"""
Created on 09 Nov 2020

@author: Jade Page (jade.page@southcoastscience.com)

"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class RuntimeRecord(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_monitor_runtime"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        last_runtime = jdict.get('last_runtime')

        return RuntimeRecord(last_runtime)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, last_runtime):
        """
        Constructor
        """
        self.__last_runtime = last_runtime

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def last_runtime(self):
        return self.__last_runtime

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['last_runtime'] = self.__last_runtime

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "RuntimeRecord:{last_runtime:%s}" %  \
               self.__last_runtime
