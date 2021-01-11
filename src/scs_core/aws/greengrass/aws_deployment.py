"""
Created on 11 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""
from getpass import getpass

import boto3

from scs_core.aws.greengrass.aws_group import AWSGroup


class AWSGroupDeployer(object):

    def __init__(self, group_name):
        self.__group_name = group_name


    @staticmethod
    def create_aws_client():
        aws_region = "us-west-2"

        access_key_secret = ""
        access_key_id = input("Enter AWS Access Key ID or leave blank to use environment variables: ")
        if access_key_id:
            access_key_secret = getpass(prompt="Enter Secret AWS Access Key: ")

        if access_key_id and access_key_secret:
            client = boto3.client(
                'greengrass',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=access_key_secret,
                region_name='us-west-2'
            )
        else:
            client = boto3.client('greengrass', region_name=aws_region)

        return client

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


