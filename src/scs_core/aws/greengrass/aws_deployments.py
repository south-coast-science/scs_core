"""
Created on 21 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)

Allows the user to view deployment information for a specific group, or all groups, in the account which
the auth keys are held for.

Examples:
./aws_deployments.py -a -i2
./aws_deployments.py -g scs-bbe-532-group -i3

Example output:
{
  "group_name": "scs-bbe-532-group",
  "created_at": "2020-09-03T12:20:59.845Z",
  "deployment_type": "NewDeployment",
  "deployment_id": "41676649-b8d4-4bce-85e3-93c142a7975b"
}

"""
from scs_core.aws.greengrass.aws_group import AWSGroup
from scs_core.aws.greengrass.deployment_report import DeploymentReport

# --------------------------------------------------------------------------------------------------------------------

class AWSDeployments(object):

    def __init__(self, client, group_name=None):
        self.__group_name = group_name
        self.__client = client

    def get_all_groups(self):
        next_token = None
        group_ids = []

        while True:
            response = self.get_groups(next_token)
            if "Groups" in response:
                for item in response["Groups"]:
                    group_ids.append(item.get("Id"))
            else:
                break
            if "NextToken" in response:
                next_token = response["NextToken"]
            else:
                break

        return group_ids

    def get_groups(self, next_token):
        if next_token is None:
            response = self.__client.list_groups()
            return response
        else:
            response = self.__client.list_groups(
                NextToken=next_token
            )
            return response

    def get_deployments(self, group_ids):
        reports = []
        for id in group_ids:
            response = self.__client.list_deployments(
                GroupId=id
            )
            if "Deployments" in response:
                if len(response["Deployments"]) > 0:
                    last_deployment = response["Deployments"][0]
                    group_name = self.get_group_name(id)
                    reports.append(DeploymentReport.construct_from_aws_deployments(last_deployment, group_name))

        return reports

    def get_group_name(self, group_id):
        response = self.__client.get_group(
            GroupId=group_id
        )
        if "Name" in response:
            return response["Name"]

    def get_group_id(self, group_name):
        aws_group_info = AWSGroup(group_name, self.__client)

        datum = aws_group_info.get_group_info_from_name()
        group_id = datum.node("GroupID")

        return group_id
