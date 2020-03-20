"""
Created on 17 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"org-id": "south-coast-science-test-user", "api-key": "9fdfb841-3433-45b8-b223-3f5a283ceb8e"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class APIAuth(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "osio_api_auth.json"

    @classmethod
    def persistence_location(cls, host):
        return host.osio_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        org_id = jdict.get('org-id')
        api_key = jdict.get('api-key')

        return APIAuth(org_id, api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, org_id, api_key):
        """
        Constructor
        """
        self.__org_id = org_id                  # String
        self.__api_key = api_key                # String


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['org-id'] = self.org_id
        jdict['api-key'] = self.api_key

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def org_id(self):
        return self.__org_id


    @property
    def api_key(self):
        return self.__api_key


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "APIAuth:{org_id:%s, api_key:%s}" % (self.org_id, self.api_key)
