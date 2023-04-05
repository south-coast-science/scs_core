"""
Created on 3 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
"""

from collections import OrderedDict

from scs_core.data.array_dict import ArrayDict
from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class OPRMembership(JSONable):
    """
    classdocs
    """

    @classmethod
    def merge(cls, oprs, oups):
        org_dict = ArrayDict([(oup.opr_id, oup) for oup in sorted(oups)])

        # OrganisationPathRoots...
        return [cls(opr, org_dict.get(opr.opr_id)) for opr in oprs]


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, opr, memberships):
        """
        Constructor
        """
        self.__opr = opr                                    # OrganisationPathRoot
        self.__memberships = memberships                    # array of OrganisationUserPath


    def __lt__(self, other):
        return self.opr < other.opr


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['opr'] = self.opr
        jdict['memberships'] = self.memberships

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def opr(self):
        return self.__opr


    @property
    def memberships(self):
        return self.__memberships


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OPRMembership:{opr:%s, memberships:%s}" % \
               (self.opr, Str.collection(self.memberships))
