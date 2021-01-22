"""
Created on 21 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Deployment(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_aws(cls, group_name, jdict):
        if not group_name:
            return None

        if not jdict:
            return cls(group_name, None, None, None)

        group_name = group_name
        created_at = LocalizedDatetime.construct_from_iso8601(jdict.get('CreatedAt'))
        deployment_type = jdict.get("DeploymentType")
        deployment_id = jdict.get("DeploymentId")

        return cls(group_name, created_at, deployment_type, deployment_id)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        group_name = jdict.get('group_name')
        created_at = LocalizedDatetime.construct_from_iso8601(jdict.get('created_at'))
        deployment_type = jdict.get('deployment_type')
        deployment_id = jdict.get('deployment_id')

        return cls(group_name, created_at, deployment_type, deployment_id)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, group_name, created_at, deployment_type, deployment_id):
        """
        Constructor
        """
        self.__group_name = group_name                      # string
        self.__created_at = created_at                      # LocalizedDatetime
        self.__deployment_type = deployment_type            # string
        self.__deployment_id = deployment_id                # string


    def __lt__(self, other):
        return self.group_name < other.group_name


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['group_name'] = self.group_name
        jdict['created_at'] = None if self.created_at is None else self.created_at.as_iso8601()
        jdict['deployment_type'] = self.deployment_type
        jdict['deployment_id'] = self.deployment_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def is_current(self, datetime):
        if self.created_at is None:
            return False

        return self.created_at >= datetime


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def group_name(self):
        return self.__group_name


    @property
    def created_at(self):
        return self.__created_at


    @property
    def deployment_type(self):
        return self.__deployment_type


    @property
    def deployment_id(self):
        return self.__deployment_id


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Deployment:{group_name:%s, created_at:%s, deployment_type:%s, deployment_id:%s}" % \
               (self.group_name, self.created_at, self.deployment_type, self.deployment_id)
