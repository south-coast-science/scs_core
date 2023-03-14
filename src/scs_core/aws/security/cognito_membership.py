"""
Created on 2 Feb 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
"""

from collections import OrderedDict

from scs_core.data.array_dict import ArrayDict
from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class CognitoMembership(JSONable):
    """
    classdocs
    """

    @classmethod
    def merge(cls, cognito_accounts, org_memberships):
        org_dict = ArrayDict([(org_membership.username, org_membership) for org_membership in sorted(org_memberships)])

        # Users...
        return [cls(cognito_account, org_dict.get(cognito_account.username)) for cognito_account in cognito_accounts]


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cognito_account, memberships):
        """
        Constructor
        """
        self.__cognito_account = cognito_account            # CognitoUserIdentity or CognitoDeviceIdentity
        self.__memberships = memberships                    # array of OrganisationUser


    def __lt__(self, other):
        return self.cognito_account < other.cognito_account


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['account'] = self.cognito_account
        jdict['memberships'] = self.memberships

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cognito_account(self):
        return self.__cognito_account


    @property
    def memberships(self):
        return self.__memberships


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CognitoMembership:{cognito_account:%s, memberships:%s}" % \
               (self.cognito_account, Str.collection(self.memberships))
