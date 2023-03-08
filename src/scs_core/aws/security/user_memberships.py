"""
Created on 2 Feb 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
"""

from collections import OrderedDict

from scs_core.aws.security.cognito_user import CognitoUserIdentity

from scs_core.data.array_dict import ArrayDict
from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class UserMemberships(JSONable):
    """
    classdocs
    """

    @classmethod
    def merge(cls, cognito_users, org_users):
        org_user_dict = ArrayDict([(org_user.username, org_user) for org_user in org_users])

        # Users...
        return [cls(cognito_user, org_user_dict.get(cognito_user.username)) for cognito_user in cognito_users]


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
        return "UserMemberships:{identity:%s, memberships:%s}" % \
               (self.identity, Str.collection(self.memberships))
