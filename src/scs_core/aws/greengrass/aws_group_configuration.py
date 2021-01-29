"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION The aws_group_configurator is a class used by aws_group_setup to collate information and make requests to
the amazon greengrass API. It is dependent on aws_json_reader to collect information.
"""

import grp
import json
import os

from collections import OrderedDict

from scs_core.aws.config.project import Project
from scs_core.aws.greengrass.aws_group import AWSGroup
from scs_core.aws.greengrass.gg_errors import ProjectMissingError

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import PersistentJSONable
from scs_core.data.path_dict import PathDict

from scs_core.sys.logging import Logging
from scs_core.sys.system_id import SystemID


# --------------------------------------------------------------------------------------------------------------------

class AWSGroupConfiguration(PersistentJSONable):
    """
    classdocs
    """

    __CWD = os.path.dirname(os.path.realpath(__file__))

    __V1 = __CWD + "/v1"
    __V2 = __CWD + "/v2"

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "aws_group_config.json"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    @classmethod
    def construct_from_jdict(cls, jdict, default=True):
        if not jdict:
            return None

        group_name = jdict.get('group-name')
        unix_group = jdict.get('unix-group')
        ml = jdict.get('ml')

        return cls(group_name, unix_group, ml)


    @classmethod
    def construct(cls, group_name, unix_group):     # TODO: remove this
        return Project(group_name, unix_group)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, group_name, client, ml=False):
        """
        Constructor
        """
        self.__logger = Logging.getLogger()

        group_info = None
        try:
            group_info = grp.getgrnam('ggc_user')
        except KeyError:
            self.__logger.error("Group GGC_USER not found. This may indicate an invalid system setup.")
            exit(2)

        self.__client = client
        self.__init_time = LocalizedDatetime.now().utc()
        self.__aws_info = PathDict()
        self.__ml = ml
        self.__group_name = group_name
        self.__unix_group = group_info[2]


    def __eq__(self, other):            # ignore init_time??
        try:
            return self.group_name == other.group_name and self.unix_group == other.unix_group and \
                   self.ml == other.ml

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def collect_information(self, host):
        aws_json_reader = AWSGroup(self.__group_name, self.__client)
        aws_json_reader.get_group_info_from_name()
        aws_json_reader.get_group_arns()
        self.__aws_info.append("GroupID", aws_json_reader.retrieve_node("GroupID"))
        self.__aws_info.append("GroupVersionID", aws_json_reader.retrieve_node("GroupLatestVersionID"))
        self.__aws_info.append("CoreDefinitionARN", aws_json_reader.retrieve_node("CoreDefinitionVersionArn"))
        self.__aws_info.append("FunctionDefinitionARN", aws_json_reader.retrieve_node("FunctionDefinitionVersionArn"))
        self.__aws_info.append("ResourceDefinitionARN", aws_json_reader.retrieve_node("ResourceDefinitionVersionArn"))
        self.__aws_info.append("SubscriptionDefinitionARN",
                               aws_json_reader.retrieve_node("SubscriptionDefinitionVersionArn"))

        temp = SystemID.load(host)
        device = temp.topic_label()
        temp_json = temp.as_json()
        self.__aws_info.append("SystemID", temp_json['system-sn'])  # can only run on a setup device

        project = Project.load(host)

        if not project:
            raise ProjectMissingError()

        else:
            project_json = project.as_json()
            device_path = project_json["device-path"] + "/" + str(device)
            self.__aws_info.append("LocationPath", project_json["location-path"])
            self.__aws_info.append("DevicePath", device_path)


    # ----------------------------------------------------------------------------------------------------------------

    def define_aws_group_resources(self, host):
        # Setup default JSON
        if self.__ml:
            j_file = os.path.join(self.__V2, 'gg_resources_ml.json')
        else:
            j_file = os.path.join(self.__V1, 'gg_resources.json')
        with open(j_file) as f:
            data = f.read()
        # Edit JSON for device
        system_id = str(self.__aws_info.node("SystemID"))
        temp = host.home_path()
        group_owner_name = temp.split("/")[2]
        scs_path = host.scs_path()
        r_data = json.loads(data)
        r_data["Name"] = ("Resources-" + system_id)  # Edit resources name
        r_data["InitialVersion"]["Resources"][0]["Id"] = (
                system_id + "-data-volume")  # Edit resource name
        r_data["InitialVersion"]["Resources"][0]["ResourceDataContainer"]["LocalVolumeResourceData"][
            "GroupOwnerSetting"]["AutoAddGroupOwner"] = False
        r_data["InitialVersion"]["Resources"][0]["ResourceDataContainer"]["LocalVolumeResourceData"][
            "SourcePath"] = scs_path
        r_data["InitialVersion"]["Resources"][0]["ResourceDataContainer"]["LocalVolumeResourceData"][
            "GroupOwnerSetting"]["GroupOwner"] = group_owner_name

        if self.__ml:
            r_data["InitialVersion"]["Resources"][1]["Id"] = (
                (system_id + "-ml-pm1"))  # Edit resource name
            r_data["InitialVersion"]["Resources"][2]["Id"] = (
                (system_id + "-ml-pm2p5"))  # Edit resource name
            r_data["InitialVersion"]["Resources"][3]["Id"] = (
                (system_id + "-ml-pm10"))  # Edit resource name
            r_data["InitialVersion"]["Resources"][4]["Id"] = (
                (system_id + "-ml-no2"))  # Edit resource name

        # Send request
        self.__logger.info("Creating resource definition")
        self.__logger.info(r_data)

        response = self.__client.create_resource_definition(InitialVersion=r_data["InitialVersion"])
        self.__aws_info.append("NewResourceARN", response["LatestVersionArn"])

        self.__logger.info(response)


    # ----------------------------------------------------------------------------------------------------------------

    def define_aws_group_functions(self):
        # Get template JSON
        if self.__ml:
            j_file = os.path.join(self.__V1, 'gg_functions_ml.json')
        else:
            j_file = os.path.join(self.__V1, 'gg_functions.json')
        with open(j_file) as f:
            data = f.read()
        # Update JSON for device
        system_id = str(self.__aws_info.node("SystemID"))
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

            f_data["InitialVersion"]["Functions"][3]["Id"] = (system_id + "-GasInference")
            f_data["InitialVersion"]["Functions"][3]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][
                0]["ResourceId"] = data_volume_name
            f_data["InitialVersion"]["Functions"][3]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][
                1]["ResourceId"] = (system_id + "-ml-no2")

        self.__logger.info("Creating function definition")
        self.__logger.info(f_data)

        # Create request
        response = self.__client.create_function_definition(InitialVersion=f_data["InitialVersion"])
        self.__aws_info.append("NewFunctionARN", response["LatestVersionArn"])

        self.__logger.info(response)


    # ----------------------------------------------------------------------------------------------------------------

    def define_aws_group_subscriptions(self):
        # Get template JSON
        j_file = os.path.join(self.__V1, 'gg_subscriptions.json')
        with open(j_file) as f:
            data = f.read()

        # Edit for device
        system_id = str(self.__aws_info.node("SystemID"))
        s_data = json.loads(data)
        s_data["InitialVersion"]["Subscriptions"][0]["Id"] = (system_id + "-particulates-subscription")
        s_data["InitialVersion"]["Subscriptions"][1]["Id"] = (system_id + "-control-from-cloud-subscription")
        s_data["InitialVersion"]["Subscriptions"][2]["Id"] = (system_id + "-climate-subscription")
        s_data["InitialVersion"]["Subscriptions"][3]["Id"] = (system_id + "-status-subscription")
        s_data["InitialVersion"]["Subscriptions"][4]["Id"] = (system_id + "-control-to-cloud-subscription")
        s_data["InitialVersion"]["Subscriptions"][5]["Id"] = (system_id + "-gases-subscription")

        s_data["InitialVersion"]["Subscriptions"][0]["Subject"] = (
                self.__aws_info.node("LocationPath") + "/particulates")
        s_data["InitialVersion"]["Subscriptions"][1]["Subject"] = (self.__aws_info.node("DevicePath") + "/control")
        s_data["InitialVersion"]["Subscriptions"][2]["Subject"] = (self.__aws_info.node("LocationPath") + "/climate")
        s_data["InitialVersion"]["Subscriptions"][3]["Subject"] = (self.__aws_info.node("DevicePath") + "/status")
        s_data["InitialVersion"]["Subscriptions"][4]["Subject"] = (self.__aws_info.node("DevicePath") + "/control")
        s_data["InitialVersion"]["Subscriptions"][5]["Subject"] = (self.__aws_info.node("LocationPath") + "/gases")

        self.__logger.info("Creating sub definition")
        self.__logger.info(s_data)

        # Send request
        response = self.__client.create_subscription_definition(InitialVersion=s_data["InitialVersion"])
        self.__aws_info.append("NewSubscriptionARN", response["LatestVersionArn"])

        self.__logger.info(response)


    def define_aws_logger(self):
        j_file = os.path.join(self.__V2, 'gg_logger.json')
        with open(j_file) as f:
            data = f.read()
        system_id = str(self.__aws_info.node("SystemID"))
        l_data = json.loads(data)

        l_data["InitialVersion"]["Loggers"][0]["Id"] = (system_id + "-lambda-logger")

        self.__logger.info("Creating logger definition")
        self.__logger.info(l_data)

        response = self.__client.create_logger_definition(InitialVersion=l_data["InitialVersion"])
        self.__aws_info.append("NewLoggerARN", response["LatestVersionArn"])

        self.__logger.info(response)


    # ----------------------------------------------------------------------------------------------------------------

    def create_aws_group_definition(self):
        self.__logger.info("Creating group definition")
        self.__logger.info(self.__aws_info.node("GroupID"))

        response = self.__client.create_group_version(
            CoreDefinitionVersionArn=self.__aws_info.node("CoreDefinitionARN"),
            FunctionDefinitionVersionArn=self.__aws_info.node("NewFunctionARN"),
            GroupId=self.__aws_info.node("GroupID"),
            ResourceDefinitionVersionArn=self.__aws_info.node("NewResourceARN"),
            SubscriptionDefinitionVersionArn=self.__aws_info.node("NewSubscriptionARN"),
            # LoggerDefinitionVersionArn=self.__aws_info.node("NewLoggerARN"),
        )

        self.__logger.info(response)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict["time-initiated"] = self.init_time
        jdict['group-name'] = self.group_name
        jdict['unix-group'] = self.unix_group
        jdict['ml'] = self.ml

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def init_time(self):
        return self.__init_time


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
        return "AWSGroupConfiguration:{group_name%s, unix_group:%d, ml:%s}" % \
               (self.group_name, self.unix_group, self.ml)
