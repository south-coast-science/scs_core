"""
Created on 30 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
  "error": {
    "body-params": {
      "client-id": "disallowed-key",
      "org-id": "disallowed-key",
      "owner-id": "disallowed-key"
    }
  }
}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Error(JSONable):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        try:
            body_params = jdict.get('body-params')
        except AttributeError:
            return jdict            # a non-JSON string was provided

        return Error(body_params)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, body_params):
        """
        Constructor
        """
        self.__body_params = body_params    # dict of field: message


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['body-params'] = self.body_params

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def body_params(self):
        return self.__body_params


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Error:{body_params:%s}" % self.body_params
