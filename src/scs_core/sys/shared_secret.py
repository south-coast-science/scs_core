"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://stackoverflow.com/questions/2257441/
random-string-generation-with-upper-case-letters-and-digits-in-python/23728630#23728630

example document:
{"key": "sxBhncFybpbMwZUa"}
"""

import random
import string

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class SharedSecret(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "shared_secret.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    __KEY_LENGTH = 16

    @classmethod
    def generate(cls):
        return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits)
                       for _ in range(cls.__KEY_LENGTH))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        key = jdict.get('key')

        return SharedSecret(key)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, key):
        """
        Constructor
        """
        super().__init__()

        self.__key = key            # String


    def __eq__(self, other):
        try:
            return self.key == other.key

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['key'] = self.key

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def key(self):
        return self.__key


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SharedSecret:{key:%s}" % self.key
