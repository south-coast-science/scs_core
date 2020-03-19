"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"endpoint": "xy1eszuu23.execute-api.us-west-2.amazonaws.com", "api-key": "de92c5ff-b47a-4cc4-a04c-62d684d74a1f"}
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
    def persistence_location(cls, host):
        return host.aws_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        endpoint = jdict.get('endpoint')
        api_key = jdict.get('api-key')

        return APIAuth(endpoint, api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, endpoint, api_key):
        """
        Constructor
        """
        self.__endpoint = endpoint              # String
        self.__api_key = api_key                # String


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['endpoint'] = self.endpoint
        jdict['api-key'] = self.api_key

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def endpoint(self):
        return self.__endpoint


    @property
    def api_key(self):
        return self.__api_key


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "APIAuth:{endpoint:%s, api_key:%s}" % (self.endpoint, self.api_key)
