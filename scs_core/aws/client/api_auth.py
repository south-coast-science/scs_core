"""
Created on 6 Nov 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"api-key": "de92c5ff-b47a-4cc4-a04c-62d684d74a1f"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class APIAuth(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "aws_api_auth.json"

    @classmethod
    def filename(cls, host):
        return host.aws_dir() + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        api_key = jdict.get('api-key')

        return APIAuth(api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, api_key):
        """
        Constructor
        """
        super().__init__()

        self.__api_key = api_key                # String


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['api-key'] = self.api_key

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def api_key(self):
        return self.__api_key


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "APIAuth:{api_key:%s}" % self.api_key
