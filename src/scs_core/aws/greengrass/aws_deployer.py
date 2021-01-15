"""
Created on 11 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""

from scs_core.aws.greengrass.aws_group import AWSGroup


# --------------------------------------------------------------------------------------------------------------------

class AWSGroupDeployer(object):
    """
    classdocs
    """

    BUILDING =      "Building"
    IN_PROGRESS =   "InProgress"
    SUCCESS =       "Success"
    FAILURE =       "Failure"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, group_name, client):
        self.__group_name = group_name
        self.__client = client


    # ----------------------------------------------------------------------------------------------------------------

    def retrieve_deployment_info(self, client):
        aws_group_info = AWSGroup(self.__group_name, client)

        datum = aws_group_info.get_group_info_from_name()
        group_id = datum.node("GroupID")
        group_version_id = datum.node("GroupLatestVersionID")

        return group_id, group_version_id


    def deploy(self):
        group_id, group_version_id = self.retrieve_deployment_info(self.__client)

        response = self.__client.create_deployment(
            DeploymentType="NewDeployment",
            GroupId=group_id,
            GroupVersionId=group_version_id
        )

        return response


    def status(self, response):
        group_id, _ = self.retrieve_deployment_info(self.__client)

        w_response = self.__client.get_deployment_status(
            DeploymentId=response.get("DeploymentId"),
            GroupId=group_id
        )

        return w_response.get("DeploymentStatus")


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AWSGroupDeployer:{group_name:%s, client:%s}" % (self.__group_name, self.__client)
