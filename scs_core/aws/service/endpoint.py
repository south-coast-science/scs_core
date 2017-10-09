"""
Created on 4 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"host": "asrfh6e5j5ecz.iot.us-west-2.amazonaws.com"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class Endpoint(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "endpoint.json"

    @classmethod
    def filename(cls, host):
        return host.aws_dir() + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        endpoint_host = jdict.get('host')

        return Endpoint(endpoint_host)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, endpoint_host):
        """
        Constructor
        """
        super().__init__()

        self.__endpoint_host = endpoint_host                  # String


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['host'] = self.endpoint_host

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def endpoint_host(self):
        return self.__endpoint_host


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Endpoint:{endpoint_host:%s}" % self.endpoint_host
