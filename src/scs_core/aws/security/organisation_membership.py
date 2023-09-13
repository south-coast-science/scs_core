"""
Created on 13 Sep 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"organisation": {"OrgID": 11, "Label": "CEPEMAR", "LongName": "CEPEMAR", "URL": "http://cepemar.com",
"Owner": "felipe.tatagiba@cepemar.com", "ParentID": null}, "children": [
{"OrgID": 82, "Label": "Vale", "LongName": "Vale S.A.", "URL": "http://www.vale.com/",
"Owner": "felipe.tatagiba@cepemar.com", "ParentID": 11}]}
"""

from collections import OrderedDict

from scs_core.data.array_dict import ArrayDict
from scs_core.data.json import JSONable
from scs_core.data.str import Str


# --------------------------------------------------------------------------------------------------------------------

class OrganisationMembership(JSONable):
    """
    classdocs
    """

    @classmethod
    def merge(cls, organisations, org_children):
        org_dict = ArrayDict([(org_member.parent_id, org_member) for org_member in sorted(org_children)])

        # Accounts...
        return [cls(organisation, org_dict.get(organisation.org_id)) for organisation in organisations]


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, organisation, children):
        """
        Constructor
        """
        self.__organisation = organisation              # Organisation
        self.__children = children                      # array of Organisation


    def __lt__(self, other):
        return self.organisation < other.organisation


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['organisation'] = self.organisation
        jdict['children'] = self.children

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def organisation(self):
        return self.__organisation


    @property
    def children(self):
        return self.__children


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "OrganisationMembership:{organisation:%s, children:%s}" % \
               (self.organisation, Str.collection(self.children))
