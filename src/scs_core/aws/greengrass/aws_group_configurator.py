"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION The aws_group_configurator is a class used by aws_group_setup to collate information and make requests to
the amazon greengrass API. It's dependent on aws_json_reader to collect information
"""

import grp
import json
import sys
import os

from collections import OrderedDict
from scs_core.aws.greengrass.gg_exceptions import ProjectMissingError
from scs_core.data.datetime import LocalizedDatetime
from scs_core.aws.config.project import Project
from scs_core.data.json import PersistentJSONable
from scs_core.sys.system_id import SystemID
from scs_core.aws.greengrass.aws_group import AWSGroup
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

class AWSGroupConfigurator(PersistentJSONable):
    __FILENAME = "aws_group_config.json"

    @classmethod
    def persistence_location(cls, host):
        return host.aws_dir(), cls.__FILENAME

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        group_name = jdict.get('group-name')
        unix_group = jdict.get('unix-group')
        ml = jdict.get('ml')

        return AWSGroupConfigurator(group_name, unix_group, ml)

    @classmethod
    def construct(cls, group_name, unix_group):
        return Project(group_name, unix_group)

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict["time-initiated"] = self.__init_time
        jdict['group-name'] = self.__group_name
        jdict['unix-group'] = self.__unix_group
        jdict['ml'] = self.__ml

        return jdict

    # ----------------------------------------------------------------------------------------------------------------
    def __init__(self, group_name, client, ml=False):
        """
        Constructor
        """
        groupinfo = grp.getgrnam('ggc_user')
        self.__client = client
        self.__init_time = LocalizedDatetime.now().utc()
        self.__awsinfo = PathDict()
        self.__ml = ml
        self.__group_name = group_name
        self.__unix_group = groupinfo[2]

    # ----------------------------------------------------------------------------------------------------------------
    def collect_information(self, host):
        aws_json_reader = AWSGroup(self.__group_name, self.__client)
        aws_json_reader.get_group_info_from_name()
        aws_json_reader.get_group_arns()
        self.__awsinfo.append("GroupID", aws_json_reader.retrieve_node("GroupID"))
        self.__awsinfo.append("GroupVersionID", aws_json_reader.retrieve_node("GroupLatestVersionID"))
        self.__awsinfo.append("CoreDefinitionARN", aws_json_reader.retrieve_node("CoreDefinitionVersionArn"))
        self.__awsinfo.append("FunctionDefinitionARN", aws_json_reader.retrieve_node("FunctionDefinitionVersionArn"))
        self.__awsinfo.append("ResourceDefinitionARN", aws_json_reader.retrieve_node("ResourceDefinitionVersionArn"))
        self.__awsinfo.append("SubscriptionDefinitionARN",
                              aws_json_reader.retrieve_node("SubscriptionDefinitionVersionArn"))

        temp = SystemID.load(host)
        device = temp.topic_label()
        temp_json = temp.as_json()
        self.__awsinfo.append("SystemID", temp_json['system-sn'])  # can only run on a setup device

        project = Project.load(host)
        if not project:
            raise ProjectMissingError()
            return
        else:
            project_json = project.as_json()
            device_path = project_json["device-path"] + "/" + str(device)
            self.__awsinfo.append("LocationPath", project_json["location-path"])
            self.__awsinfo.append("DevicePath", device_path)

    # ----------------------------------------------------------------------------------------------------------------
    def define_aws_group_resources(self, host):
        # Setup default JSON
        if self.__ml:
            j_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gg_resources_ml.json')
        else:
            j_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gg_resources.json')
        with open(j_file) as f:
            data = f.read()
        # Edit JSON for device
        system_id = str(self.__awsinfo.node("SystemID"))
        temp = host.home_dir()
        group_owner_name = temp.split("/")[2]
        scs_dir = host.scs_dir()
        unix_group_number = str(self.__unix_group)
        r_data = json.loads(data)
        r_data["Name"] = ("Resources-" + system_id)  # Edit resources name
        r_data["InitialVersion"]["Resources"][0]["Id"] = (
                system_id + "-data-volume")  # Edit resource name
        r_data["InitialVersion"]["Resources"][0]["ResourceDataContainer"]["LocalVolumeResourceData"][
            "GroupOwnerSetting"]["AutoAddGroupOwner"] = False
        r_data["InitialVersion"]["Resources"][0]["ResourceDataContainer"]["LocalVolumeResourceData"][
            "SourcePath"] = scs_dir
        r_data["InitialVersion"]["Resources"][0]["ResourceDataContainer"]["LocalVolumeResourceData"][
            "GroupOwnerSetting"]["GroupOwner"] = group_owner_name

        if self.__ml:
            r_data["InitialVersion"]["Resources"][1]["Id"] = (
                (system_id + "-ml-pm1"))  # Edit resource name
            r_data["InitialVersion"]["Resources"][2]["Id"] = (
                (system_id + "-ml-pm2p5"))  # Edit resource name
            r_data["InitialVersion"]["Resources"][3]["Id"] = (
                (system_id + "-ml-pm10"))  # Edit resource name
            r_data["InitialVersion"]["Resources"][1]["ResourceDataContainer"][
                "SageMakerMachineLearningModelResourceData"]["OwnerSetting"]["GroupOwner"] = (
                unix_group_number)
            r_data["InitialVersion"]["Resources"][2]["ResourceDataContainer"][
                "SageMakerMachineLearningModelResourceData"]["OwnerSetting"]["GroupOwner"] = (
                unix_group_number)
            r_data["InitialVersion"]["Resources"][3]["ResourceDataContainer"][
                "SageMakerMachineLearningModelResourceData"]["OwnerSetting"]["GroupOwner"] = (
                unix_group_number)
        # Send request
        response = self.__client.create_resource_definition(InitialVersion=r_data["InitialVersion"])
        self.__awsinfo.append("NewResourceARN", response["LatestVersionArn"])
        print(response, file=sys.stderr)

    # ----------------------------------------------------------------------------------------------------------------
    def define_aws_group_functions(self):
        # Get template JSON
        if self.__ml:
            j_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gg_functions_ml.json')
        else:
            j_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gg_functions.json')
        with open(j_file) as f:
            data = f.read()
        # Update JSON for device
        system_id = str(self.__awsinfo.node("SystemID"))
        data_volume_name = (system_id + "-data-volume")
        f_data = json.loads(data)
        f_data["InitialVersion"]["Functions"][0]["Id"] = (system_id + "-ControlSubscriber")
        f_data["InitialVersion"]["Functions"][1]["Id"] = (system_id + "-TopicPublisher")

        f_data["InitialVersion"]["Functions"][0]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][0][
            "ResourceId"] = data_volume_name
        f_data["InitialVersion"]["Functions"][1]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][0][
            "ResourceId"] = data_volume_name
        if self.__ml:
            f_data["InitialVersion"]["Functions"][2]["Id"] = (system_id + "-PMxInference")
            f_data["InitialVersion"]["Functions"][2]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][
                0]["ResourceId"] = data_volume_name
            f_data["InitialVersion"]["Functions"][2]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][
                1]["ResourceId"] = (system_id + "-ml-pm1")
            f_data["InitialVersion"]["Functions"][2]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][
                2]["ResourceId"] = (system_id + "-ml-pm2p5")
            f_data["InitialVersion"]["Functions"][2]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][
                3]["ResourceId"] = (system_id + "-ml-pm10")

        # Create request
        response = self.__client.create_function_definition(InitialVersion=f_data["InitialVersion"])
        self.__awsinfo.append("NewFunctionARN", response["LatestVersionArn"])
        print(response, file=sys.stderr)

    # ----------------------------------------------------------------------------------------------------------------
    def define_aws_group_subscriptions(self):
        # Get template JSON
        j_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gg_subscriptions.json')
        with open(j_file) as f:
            data = f.read()

        # Edit for device
        system_id = str(self.__awsinfo.node("SystemID"))
        s_data = json.loads(data)
        s_data["InitialVersion"]["Subscriptions"][0]["Id"] = (system_id + "-particulates-subscription")
        s_data["InitialVersion"]["Subscriptions"][1]["Id"] = (system_id + "-control-from-cloud-subscription")
        s_data["InitialVersion"]["Subscriptions"][2]["Id"] = (system_id + "-climate-subscription")
        s_data["InitialVersion"]["Subscriptions"][3]["Id"] = (system_id + "-status-subscription")
        s_data["InitialVersion"]["Subscriptions"][4]["Id"] = (system_id + "-control-to-cloud-subscription")
        s_data["InitialVersion"]["Subscriptions"][5]["Id"] = (system_id + "-gases-subscription")

        s_data["InitialVersion"]["Subscriptions"][0]["Subject"] = (
                self.__awsinfo.node("LocationPath") + "/particulates")
        s_data["InitialVersion"]["Subscriptions"][1]["Subject"] = (self.__awsinfo.node("DevicePath") + "/control")
        s_data["InitialVersion"]["Subscriptions"][2]["Subject"] = (self.__awsinfo.node("LocationPath") + "/climate")
        s_data["InitialVersion"]["Subscriptions"][3]["Subject"] = (self.__awsinfo.node("DevicePath") + "/status")
        s_data["InitialVersion"]["Subscriptions"][4]["Subject"] = (self.__awsinfo.node("DevicePath") + "/control")
        s_data["InitialVersion"]["Subscriptions"][5]["Subject"] = (self.__awsinfo.node("LocationPath") + "/gases")

        # Send request
        response = self.__client.create_subscription_definition(InitialVersion=s_data["InitialVersion"])
        self.__awsinfo.append("NewSubscriptionARN", response["LatestVersionArn"])
        print(response, file=sys.stderr)

    # ----------------------------------------------------------------------------------------------------------------
    def create_aws_group_definition(self):
        response = self.__client.create_group_version(
            CoreDefinitionVersionArn=self.__awsinfo.node("CoreDefinitionARN"),
            FunctionDefinitionVersionArn=self.__awsinfo.node("NewFunctionARN"),
            GroupId=self.__awsinfo.node("GroupID"),
            ResourceDefinitionVersionArn=self.__awsinfo.node("NewResourceARN"),
            SubscriptionDefinitionVersionArn=self.__awsinfo.node("NewSubscriptionARN"),
        )
        print(response, file=sys.stderr)

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def group_name(self):
        return self.__group_name

    @property
    def unix_group(self):
        return self.__unix_group

    @property
    def ml(self):
        return self.__ml

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Project:{group_name%s, unix_group:%d, ml:%s}" % (self.group_name, self.unix_group, self.ml)
