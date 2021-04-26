"""
Created on 08 Feb 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""

import json
import os
import re

from collections import OrderedDict

from scs_core.aws.greengrass.aws_group import AWSGroup

from scs_core.data.path_dict import PathDict

from scs_core.estate.configuration import Configuration

from scs_core.sys.logging import Logging
from scs_core.sys.system_id import SystemID


# --------------------------------------------------------------------------------------------------------------------

class AWSGroupCloner(object):
    """
    classdocs
    """

    __CWD = os.path.dirname(os.path.realpath(__file__))
    __V1 = __CWD + "/v1"

    __GAS_FUNCTION = "GasInference"
    __PARTS_FUNCTION = "PMxInference"

    __GAS_RESOURCE = "ML-NO2"
    __PARTS_RESOURCE = ["ML-PM1", "ML-PM10", "ML-PM2P5"]

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, origin_group_name, dest_group_name, client, gas, parts):
        self.__gas = gas
        self.__parts = parts

        self.__origin_group_name = origin_group_name
        self.__origin_group_number = None
        self.__dest_group_name = dest_group_name
        self.__dest_group_number = None
        self.__origin_owner = None
        self.__dest_owner = None

        self.__logger = Logging.getLogger()

        self.__client = client
        self.__aws_group_info = AWSGroup(self.__origin_group_name, self.__client)

        self.__aws_info = PathDict()

        self.__arns = None
        self.__origin_function_info = None
        self.__origin_resource_info = None

        self.__dest_function_info = None
        self.__dest_resource_info = None
        self.__dest_loc_path = None
        self.__dest_dev_path = None
        self.__dest_group_id = None


    # ----------------------------------------------------------------------------------------------------------------

    def retrieve_group_info(self):
        aws_json_reader = AWSGroup(self.__origin_group_name, self.__client)
        aws_json_reader.get_group_info_from_name()
        aws_json_reader.get_group_arns()
        aws_json_reader.get_function_definition()
        aws_json_reader.get_logger_definition()
        aws_json_reader.get_resource_definition()
        aws_json_reader.get_subscription_definition_version()

        origin_info = aws_json_reader.return_verbose_info()

        function_info = origin_info.node("Function Definition Response")
        self.__origin_function_info = function_info["Definition"]

        resource_info = origin_info.node("Resource Definition Response")
        self.__origin_resource_info = resource_info["Definition"]

        aws_json_reader = AWSGroup(self.__dest_group_name, self.__client)
        group_info = aws_json_reader.get_group_info_from_name()
        group_id = group_info.node("GroupID")
        self.__dest_group_id = group_id
        aws_json_reader.get_group_arns()
        self.__aws_info.append("CoreDefinitionARN", aws_json_reader.retrieve_node("CoreDefinitionVersionArn"))


    def update_function_info(self):
        new_dict = []

        for item in self.__origin_function_info["Functions"]:
            resource = json.dumps(item)

            # There's probably a more elegant way to do this:
            if self.__GAS_FUNCTION in resource:
                if not self.__gas:
                    continue

            if self.__PARTS_FUNCTION in resource:
                if not self.__parts:
                    continue

            n_resource = resource.replace(self.__origin_group_number, self.__dest_group_number)
            new_dict.append(json.loads(n_resource))

        self.__dest_function_info = new_dict


    def update_resource_info(self):
        new_dict = []

        for item in self.__origin_resource_info["Resources"]:

            if self.__GAS_RESOURCE in item["Name"]:
                if not self.__gas:
                    continue

            if item["Name"] in self.__PARTS_RESOURCE:
                if not self.__parts:
                    continue

            resource = json.dumps(item)
            no_resource = resource.replace(self.__origin_group_number, self.__dest_group_number)
            n_resource = no_resource.replace(self.__origin_owner, self.__dest_owner)
            new_dict.append(json.loads(n_resource))

        self.__dest_resource_info = new_dict


    def validate_names(self):
        reg = re.compile("scs-(\\w+)-(\\d{3})-group")
        is_valid = reg.fullmatch(self.__origin_group_name)
        if not is_valid:
            return False

        is_valid = reg.fullmatch(self.__dest_group_name)
        if not is_valid:
            return False

        return True


    def create_resources_version(self):
        jdict = OrderedDict()

        resources = self.__dest_resource_info
        resource_container_name = "Resources-" + self.__dest_group_number
        jdict['Name'] = resource_container_name

        jdict_init = OrderedDict()
        jdict_init['Resources'] = resources

        jdict['InitialVersion'] = jdict_init

        # Send request
        self.__logger.info("Creating resource definition")
        self.__logger.debug(jdict)

        response = self.__client.create_resource_definition(InitialVersion=jdict["InitialVersion"])
        self.__aws_info.append("NewResourceARN", response["LatestVersionArn"])

        self.__logger.debug(response)


    def create_function_version(self):
        jdict = OrderedDict()

        functions = self.__dest_function_info

        jdict_init = OrderedDict()
        jdict_init['Functions'] = functions

        jdict['InitialVersion'] = jdict_init

        self.__logger.info("Creating function definition")
        self.__logger.debug(jdict)

        # Create request
        response = self.__client.create_function_definition(InitialVersion=jdict["InitialVersion"])
        self.__aws_info.append("NewFunctionARN", response["LatestVersionArn"])

        self.__logger.debug(response)


    def get_project_locations(self, host):
        system_id = SystemID.load(host)

        if system_id is None:
            self.__logger.error('SystemID not available.')
            return False

        configuration = Configuration.load(host)

        self.__dest_loc_path = configuration.aws_project.location_path
        self.__dest_dev_path = configuration.aws_project.device_path

        return True


    def create_subscription_version(self):
        # Get template JSON
        j_file = os.path.join(self.__V1, 'gg_subscriptions.json')
        with open(j_file) as f:
            data = f.read()

        # Edit for device
        group_number = self.__dest_group_number
        device_path = self.__dest_dev_path
        loc_path = self.__dest_loc_path

        s_data = json.loads(data)
        s_data["InitialVersion"]["Subscriptions"][0]["Id"] = (group_number + "-particulates-subscription")
        s_data["InitialVersion"]["Subscriptions"][1]["Id"] = (group_number + "-control-from-cloud-subscription")
        s_data["InitialVersion"]["Subscriptions"][2]["Id"] = (group_number + "-climate-subscription")
        s_data["InitialVersion"]["Subscriptions"][3]["Id"] = (group_number + "-status-subscription")
        s_data["InitialVersion"]["Subscriptions"][4]["Id"] = (group_number + "-control-to-cloud-subscription")
        s_data["InitialVersion"]["Subscriptions"][5]["Id"] = (group_number + "-gases-subscription")

        s_data["InitialVersion"]["Subscriptions"][0]["Subject"] = (loc_path + "/particulates")
        s_data["InitialVersion"]["Subscriptions"][1]["Subject"] = (device_path + "/control")
        s_data["InitialVersion"]["Subscriptions"][2]["Subject"] = (loc_path + "/climate")
        s_data["InitialVersion"]["Subscriptions"][3]["Subject"] = (device_path + "/status")
        s_data["InitialVersion"]["Subscriptions"][4]["Subject"] = (device_path + "/control")
        s_data["InitialVersion"]["Subscriptions"][5]["Subject"] = (loc_path + "/gases")

        self.__logger.info("Creating sub definition")
        self.__logger.debug(s_data)

        # Send request
        response = self.__client.create_subscription_definition(InitialVersion=s_data["InitialVersion"])
        self.__aws_info.append("NewSubscriptionARN", response["LatestVersionArn"])

        self.__logger.debug(response)


    def create_aws_group_definition(self):
        self.__logger.info("Creating group definition")

        response = self.__client.create_group_version(
            CoreDefinitionVersionArn=self.__aws_info.node("CoreDefinitionARN"),
            FunctionDefinitionVersionArn=self.__aws_info.node("NewFunctionARN"),
            GroupId=self.__dest_group_id,
            ResourceDefinitionVersionArn=self.__aws_info.node("NewResourceARN"),
            SubscriptionDefinitionVersionArn=self.__aws_info.node("NewSubscriptionARN"),
        )

        self.__logger.info(response)


    def run(self, host):
        temp = self.__origin_group_name.split("-")
        self.__origin_group_number = temp[2]
        self.__origin_owner = "pi" if temp[1] == "rpi" else "scs"

        temp = self.__dest_group_name.split("-")
        self.__dest_group_number = temp[2]
        self.__dest_owner = "pi" if temp[1] == "rpi" else "scs"

        self.retrieve_group_info()

        self.update_function_info()
        self.update_resource_info()

        self.create_resources_version()
        self.create_function_version()

        if not self.get_project_locations(host):
            return False

        self.create_subscription_version()

        self.create_aws_group_definition()

        return True  # Succeeded probably
