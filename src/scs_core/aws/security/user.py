"""
Created on 2 Feb 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
"""

from collections import OrderedDict

from scs_core.aws.security.cognito_user import CognitoUserIdentity

from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class User(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, identity: CognitoUserIdentity, memberships):
        """
        Constructor
        """
        self.__identity = identity                          # CognitoUserIdentity
        self.__memberships = memberships                    # array of OrganisationUser


    def __lt__(self, other):
        return self.identity < other.identity


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['identity'] = self.identity
        jdict['memberships'] = self.memberships

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def identity(self):
        return self.__identity


    @property
    def memberships(self):
        return self.__memberships


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "User:{identity:%s, memberships:%s}" % \
               (self.identity, Str.collection(self.memberships))
