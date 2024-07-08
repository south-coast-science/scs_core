"""
Created on 5 Jul 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Extracting the Greengrass group definition for the device... used by root provisioning.

example JSON:
<see /greengrass/ggc/deployment/group/group.json>
"""

from scs_core.data.json import PersistentJSONable
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class AWSGroupVersion(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __DIR = "/greengrass/ggc/deployment/group"
    __FILENAME = "group.json"

    @classmethod
    def persistence_location(cls):
        return cls.__DIR, cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        return cls(PathDict(jdict))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path_dict: PathDict):
        """
        Constructor
        """
        super().__init__()

        self.__path_dict = path_dict                        # PathDict


    # ----------------------------------------------------------------------------------------------------------------
    # core...

    @property
    def core(self):
        for item in self.__path_dict.node('Cores'):
            return item                                     # first item only

        return None


    @property
    def core_arn(self):
        return self.core['thingArn']


    @property
    def core_name(self):
        return self.core_arn.split('/')[-1]


    @property
    def group_name(self):
        return self.core_name.replace('core', 'group')


    # ----------------------------------------------------------------------------------------------------------------
    # logging...

    @property
    def loggers(self):
        return self.__path_dict.node('GroupDefinitions.Logging.Content')


    @property
    def greengrass_log_level(self):
        item = self.__logging_component('GreengrassSystem')
        return item['Level']


    @greengrass_log_level.setter
    def greengrass_log_level(self, level):
        item = self.__logging_component('GreengrassSystem')
        item['Level'] = level


    @property
    def lambda_log_level(self):
        item = self.__logging_component('Lambda')
        return item['Level']


    @lambda_log_level.setter
    def lambda_log_level(self, level):
        item = self.__logging_component('Lambda')
        item['Level'] = level


    def __logging_component(self, name):
        for item in self.loggers:
            if item['Component'] == name:
                return item

        raise KeyError(name)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        return self.__path_dict.dictionary


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AWSGroupVersion:{%s}" % self.__path_dict
