"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION The aws_group is a class used by aws_group_setup to collect information from the amazon greengrass
api
"""

import sys

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class AWSGroup(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, group_name, client):
        """
        Constructor
        """
        self.__client = client
        self.__group_info = PathDict()
        self.__group_info.append("GroupName", [group_name])
        self.__verbose_group_info = PathDict()


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['info'] = self.__group_info
        jdict['v-info'] = self.__verbose_group_info

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def get_group_info_from_name(self):
        groups = []

        res = self.__client.list_groups(MaxResults='1000')
        groups.extend(res["Groups"])
        while "NextToken" in res:
            res = self.__client.list_groups(MaxResults='1000', NextToken=res["NextToken"])
            groups.extend(res["Groups"])

        # print("response...", file=sys.stderr)
        # print(response, file=sys.stderr)

        for group in groups:
            this_name = group["Name"]

            if this_name != self.__group_info.node("GroupName")[0]:
                continue

            self.__group_info.append("GroupID", group["Id"])
            self.__group_info.append("GroupLatestVersionID", group["LatestVersion"])
            self.__group_info.append("LastUpdated", group["LastUpdatedTimestamp"])
            return self.__group_info

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def get_group_arns(self):
        response = self.__client.get_group_version(
            GroupId=self.__group_info.node("GroupID"),
            GroupVersionId=self.__group_info.node("GroupLatestVersionID")
        )
        v_group = PathDict(response)
        sub_v_group = v_group.node("Definition")

        if "CoreDefinitionVersionArn" in sub_v_group:
            self.__group_info.append("CoreDefinitionVersionArn",
                                     sub_v_group["CoreDefinitionVersionArn"])

        if "FunctionDefinitionVersionArn" in sub_v_group:
            self.__group_info.append("FunctionDefinitionVersionArn",
                                     sub_v_group["FunctionDefinitionVersionArn"])

        if "LoggerDefinitionVersionArn" in sub_v_group:
            self.__group_info.append("LoggerDefinitionVersionArn",
                                     sub_v_group["LoggerDefinitionVersionArn"])

        if "ResourceDefinitionVersionArn" in sub_v_group:
            self.__group_info.append("ResourceDefinitionVersionArn",
                                     sub_v_group["ResourceDefinitionVersionArn"])

        if "SubscriptionDefinitionVersionArn" in sub_v_group:
            self.__group_info.append("SubscriptionDefinitionVersionArn",
                                     sub_v_group["SubscriptionDefinitionVersionArn"])


    # ----------------------------------------------------------------------------------------------------------------

    def output_current_info(self):
        if self.__group_info.has_path("CoreDefinitionVersionArn"):
            self.get_core_definition()
        if self.__group_info.has_path("LoggerDefinitionVersionArn"):
            self.get_logger_definition()
        if self.__group_info.has_path("ResourceDefinitionVersionArn"):
            self.get_resource_definition()
        if self.__group_info.has_path("FunctionDefinitionVersionArn"):
            self.get_function_definition()
        if self.__group_info.has_path("SubscriptionDefinitionVersionArn"):
            self.get_subscription_definition_version()


    # ----------------------------------------------------------------------------------------------------------------

    def get_core_definition(self):

        if not self.__group_info.has_path("CoreDefinitionVersionArn"):
            return
        if not self.__group_info.node("CoreDefinitionVersionArn"):
            return

        arn = self.__split_id_from_version_id("core", self.__group_info.node("CoreDefinitionVersionArn"))
        response = self.__client.get_core_definition_version(
            CoreDefinitionId=arn[0],
            CoreDefinitionVersionId=arn[1]
        )
        self.__verbose_group_info.append("Core Definition Response", response)


    # ----------------------------------------------------------------------------------------------------------------

    def get_function_definition(self):
        if not self.__group_info.has_path("FunctionDefinitionVersionArn"):
            print("Group missing function definition version", file=sys.stderr)
            return

        if not self.__group_info.node("FunctionDefinitionVersionArn"):
            print("Group missing function definition version", file=sys.stderr)
            return

        arn = self.__split_id_from_version_id("function", self.__group_info.node("FunctionDefinitionVersionArn"))
        response = self.__client.get_function_definition_version(
            FunctionDefinitionId=arn[0],
            FunctionDefinitionVersionId=arn[1]
        )

        self.__verbose_group_info.append("Function Definition Response", response)


    # ----------------------------------------------------------------------------------------------------------------

    def get_logger_definition(self):

        if not self.__group_info.has_path("LoggerDefinitionVersionArn"):
            return
        if not self.__group_info.node("LoggerDefinitionVersionArn"):
            return

        arn = self.__split_id_from_version_id("logger", self.__group_info.node("LoggerDefinitionVersionArn"))
        response = self.__client.get_logger_definition_version(
            LoggerDefinitionId=arn[0],
            LoggerDefinitionVersionId=arn[1]
        )
        self.__verbose_group_info.append("Logger Definition Response", response)


    # ----------------------------------------------------------------------------------------------------------------

    def get_resource_definition(self):

        if not self.__group_info.has_path("ResourceDefinitionVersionArn"):
            return
        if not self.__group_info.node("ResourceDefinitionVersionArn"):
            return

        arn = self.__split_id_from_version_id("resources", self.__group_info.node("ResourceDefinitionVersionArn"))
        response = self.__client.get_resource_definition_version(
            ResourceDefinitionId=arn[0],
            ResourceDefinitionVersionId=arn[1]
        )
        self.__verbose_group_info.append("Resource Definition Response", response)


    # ----------------------------------------------------------------------------------------------------------------

    def get_subscription_definition_version(self):

        if not self.__group_info.has_path("SubscriptionDefinitionVersionArn"):
            return
        if not self.__group_info.node("SubscriptionDefinitionVersionArn"):
            return

        arn = self.__split_id_from_version_id("subscriptions",
                                              self.__group_info.node("SubscriptionDefinitionVersionArn"))

        response = self.__client.get_subscription_definition_version(
            SubscriptionDefinitionId=arn[0],
            SubscriptionDefinitionVersionId=arn[1]
        )
        self.__verbose_group_info.append("Subscription Definition Response", response)


    # ----------------------------------------------------------------------------------------------------------------

    def __append_to_group_info(self, path, value):
        self.__group_info.append(path, value)


    # ----------------------------------------------------------------------------------------------------------------

    def retrieve_node(self, path):
        if self.__group_info.has_path(path):
            return self.__group_info.node(path)
        else:
            return "-"

    def return_verbose_info(self):
        return self.__verbose_group_info


    # --------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __split_id_from_version_id(arn_type, combined):
        res = ""
        if arn_type == "core":
            split1 = combined.split("/cores/")
            res = split1[1].split("/versions/")
        if arn_type == "function":
            split1 = combined.split("/functions/")
            res = split1[1].split("/versions/")
        if arn_type == "logger":
            split1 = combined.split("/loggers/")
            res = split1[1].split("/versions/")
        if arn_type == "resources":
            split1 = combined.split("/resources/")
            res = split1[1].split("/versions/")
        if arn_type == "subscriptions":
            split1 = combined.split("/subscriptions/")
            res = split1[1].split("/versions/")
        return res
