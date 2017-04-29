"""
Created on 14 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.osio.client.rest_client import RESTClient
from scs_core.osio.data.schema import Schema


# --------------------------------------------------------------------------------------------------------------------

class SchemaManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key):
        """
        Constructor
        """
        self.__rest_client = RESTClient(http_client, api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def find_all(self):
        request_path = '/v2/schemas'

        # request...
        self.__rest_client.connect()

        try:
            response_jdict = self.__rest_client.get(request_path)

        finally:
            self.__rest_client.close()

        schemas = [Schema.construct_from_jdict(schema_jdict) for schema_jdict in response_jdict]

        return schemas


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SchemaManager:{rest_client:%s}" % self.__rest_client
