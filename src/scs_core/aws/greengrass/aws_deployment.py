"""
Created on 11 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""

import boto3

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.config.aws import AWS
from scs_core.aws.greengrass.aws_group import AWSGroup


# --------------------------------------------------------------------------------------------------------------------

class AWSGroupDeployer(object):

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create_aws_client():
        key = AccessKey.from_user()

        if key.ok():
            client = boto3.client(
                'greengrass',
                aws_access_key_id=key.id,
                aws_secret_access_key=key.secret,
                region_name=AWS.region()
            )

        else:
            client = boto3.client('greengrass', region_name=AWS.region())

        return client


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, group_name):
        self.__group_name = group_name


    # ----------------------------------------------------------------------------------------------------------------

    def retrieve_deployment_info(self, client):
        aws_group_info = AWSGroup(self.__group_name, client)

        datum = aws_group_info.get_group_info_from_name()
        group_id = datum.node("GroupID")
        group_version_id = datum.node("GroupLatestVersionID")

        return group_id, group_version_id


    def deploy(self):
        client = self.create_aws_client()
        group_id, group_version_id = self.retrieve_deployment_info(client)
        response = client.create_deployment(
            DeploymentType="NewDeployment",
            GroupId=group_id,
            GroupVersionId=group_version_id
        )
        return response
