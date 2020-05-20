"""
Created on 30 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.osio.data.error import Error


# --------------------------------------------------------------------------------------------------------------------

class ClientException(RuntimeError, JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, http_exception):
        try:
            jdict = json.loads(http_exception.data)
        except ValueError:
            return ClientException(None)

        try:
            error = Error.construct_from_jdict(jdict['error'])
        except KeyError:
            return ClientException(None)

        return ClientException(error)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, error, *args):
        super().__init__(*args)

        self.__error = error


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['error'] = self.error

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def error(self):
        return self.__error


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ClientException:{error:%s}" % self.error
