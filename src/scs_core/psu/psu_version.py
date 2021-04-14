"""
Created on 8 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{"id": "South Coast Science PSU", "tag": "1.0.0", "c-date": "Aug  8 2017", "c-time": "08:35:25"}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class PSUVersion(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, id, tag_jdict, compile_date=None, compile_time=None):
        tag = PSUTag.construct_from_jdict(tag_jdict)

        return cls(id, tag, compile_date, compile_time)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        id = jdict.get('id')

        tag = PSUTag.construct_from_jdict(jdict.get('tag'))

        compile_date = jdict.get('c-date')
        compile_time = jdict.get('c-time')

        return cls(id, tag, compile_date, compile_time)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id, tag, compile_date, compile_time):
        """
        Constructor
        """
        self.__id = id                                  # string
        self.__tag = tag                                # PSUTag

        self.__compile_date = compile_date              # string (Unix date)
        self.__compile_time = compile_time              # string (time)


    def __eq__(self, other):
        try:
            return self.id == other.id and self.tag == other.tag and \
                   self.compile_date == other.compile_date and self.compile_time == other.compile_time

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['id'] = self.id
        jdict['tag'] = self.tag

        jdict['c-date'] = self.compile_date
        jdict['c-time'] = self.compile_time

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def tag(self):
        return self.__tag


    @property
    def compile_date(self):
        return self.__compile_date


    @property
    def compile_time(self):
        return self.__compile_time


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PSUVersion:{id:%s, tag:%s, compile_date:%s, compile_time:%s}" \
               % (self.id, self.tag, self.compile_date, self.compile_time)


# --------------------------------------------------------------------------------------------------------------------

class PSUTag(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        items = jdict.split('.')

        device = items[0]
        api = items[1]
        patch = items[2]

        return cls(device, api, patch)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, api, patch):
        """
        Constructor
        """
        self.__device = device                  # string representation of int
        self.__api = api                        # string representation of int
        self.__patch = patch                    # string representation of int


    def __eq__(self, other):
        try:
            return self.device == other.device and self.api == other.api and self.patch == other.patch

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return '.'.join((self.device, self.api, self.patch))


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
        return "PSUTag:{device:%s, api:%s, patch:%s}" % (self.device, self.api, self.patch)
