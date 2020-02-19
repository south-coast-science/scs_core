"""
Created on 2 Jan 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

document example:
version: {"id": "SCS NDIR Type 001", "tag": "001.001.001"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class NDIRVersion(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        id = jdict.get('id')
        tag = NDIRTag.construct_from_jdict(jdict.get('tag'))

        return NDIRVersion(id, tag)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, tag):
        """
        Constructor
        """
        self.__id = id                                  # string
        self.__tag = tag                                # NDIRTag


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['id'] = self.id
        jdict['tag'] = self.tag

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def tag(self):
        return self.__tag


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRVersion:{id:%s, tag:%s}" % (self.id, self.tag)


# --------------------------------------------------------------------------------------------------------------------

class NDIRTag(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        items = jdict.split('.')

        try:
            device = int(items[0])
            api = int(items[1])
            patch = int(items[2])

        except ValueError:
            return None

        return NDIRTag(device, api, patch)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, api, patch):
        """
        Constructor
        """
        self.__device = device                  # int
        self.__api = api                        # int
        self.__patch = patch                    # int


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return '.'.join((str(self.device), str(self.api), str(self.patch)))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def device(self):
        return self.__device


    @property
    def api(self):
        return self.__api


    @property
    def patch(self):
        return self.__patch


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIRTag:{device:%s, api:%s, patch:%s}" % (self.device, self.api, self.patch)
