"""
Created on 21 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""

from scs_core.aws.data.deployment import Deployment
from scs_core.aws.greengrass.aws_group import AWSGroup


# --------------------------------------------------------------------------------------------------------------------

class AWSDeploymentReporter(object):

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client):
        self.__client = client


    # ----------------------------------------------------------------------------------------------------------------

    def get_all_group_ids(self):
        next_token = None
        group_ids = []

        while True:
            response = self.__get_groups(next_token)

            if "Groups" not in response:
                break

            for item in response["Groups"]:
                group_ids.append(item.get("Id"))

            if "NextToken" not in response:
                break

            next_token = response["NextToken"]

        return group_ids


    def get_group_id(self, group_name):
        aws_group_info = AWSGroup(group_name, self.__client)

        datum = aws_group_info.get_group_info_from_name()
        group_id = datum.node("GroupID")

        return group_id


    def get_group_names(self, group_ids, before=None):
        return [deployment.group_name for deployment in self.get_deployments(group_ids, before=before)]


    def get_deployments(self, group_ids, before=None):
        deployments = []

        for id in group_ids:
            response = self.__client.list_deployments(GroupId=id)

            if "Deployments" not in response or not response["Deployments"]:
                continue

            group_name = self.__get_group_name(id)
            last_deployment = response["Deployments"][0]
            deployment = Deployment.construct_from_aws(group_name, last_deployment)

            if deployment.before(before):
                deployments.append(deployment)

        return sorted(deployments)


    # ----------------------------------------------------------------------------------------------------------------

    def __get_groups(self, next_token):
        if next_token is None:
            return self.__client.list_groups()

        return self.__client.list_groups(NextToken=next_token)


    def __get_group_name(self, group_id):
        response = self.__client.get_group(GroupId=group_id)

        if "Name" not in response:
            return None

        return response["Name"]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AWSDeploymentReporter:{client:%s}" % self.__client
