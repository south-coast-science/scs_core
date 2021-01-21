"""
Created on 21 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""

# --------------------------------------------------------------------------------------------------------------------
from collections import OrderedDict

from scs_core.data.json import JSONable


class DeploymentReport(JSONable):

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        group_name = jdict.get('group_name')
        created_at = jdict.get('created_at')
        deployment_type = jdict.get('deployment_type')
        deployment_id = jdict.get('deployment_id')

        return cls(group_name, created_at, deployment_type, deployment_id)

    @classmethod
    def construct_from_aws_deployments(cls, deployment, group_name):
        if not deployment:
            return None

        if not group_name:
            return None

        group_name = group_name
        created_at = deployment.get("CreatedAt")
        deployment_type = deployment.get("DeploymentType")
        deployment_id = deployment.get("DeploymentId")

        return cls(group_name, created_at, deployment_type, deployment_id)

    def __init__(self, group_name, created_at, deployment_type, deployment_id):
        """
        Constructor
        """
        self.__group_name = group_name
        self.__created_at = created_at

        self.__deployment_type = deployment_type
        self.__deployment_id = deployment_id

    def as_json(self):
        jdict = OrderedDict()

        jdict['group_name'] = self.group_name
        jdict['created_at'] = self.created_at

        jdict['deployment_type'] = self.deployment_type
        jdict['deployment_id'] = self.deployment_id

        return jdict

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
