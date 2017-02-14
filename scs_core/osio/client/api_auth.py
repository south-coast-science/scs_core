"""
Created on 17 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
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
    def filename(cls, host):
        return host.SCS_OSIO + cls.__FILENAME


    @classmethod
    def load_from_host(cls, host):
        return cls.load_from_file(cls.filename(host))


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

    def save(self, host):
        PersistentJSONable.save(self, self.__class__.filename(host))


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
