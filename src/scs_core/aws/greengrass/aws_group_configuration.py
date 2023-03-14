"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

The aws_group_configurator is a class used by aws_group_setup to collate information and make requests to
the amazon greengrass API. It is dependent on aws_json_reader to collect information.

example document
{"group-name": "scs-bbe-651-group", "time-initiated": "2021-09-21T13:00:31Z", "unix-group": 987, "ml": "oE1"}
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

from scs_core.sys.filesystem import Filesystem
from scs_core.sys.logging import Logging
from scs_core.sys.system_id import SystemID


# --------------------------------------------------------------------------------------------------------------------

class AWSGroupConfiguration(PersistentJSONable):
    """
    classdocs
    """
    __CATALOGUE_NAME = 'templates'

    @classmethod
    def catalogue_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), cls.__CATALOGUE_NAME)


    @classmethod
    def templates(cls):
        return tuple(item.name for item in Filesystem.ls(cls.catalogue_location()) if item.is_directory)


    @classmethod
    def read(cls, catalogue, file):
        abs_path = os.path.join(cls.catalogue_location(), catalogue, file)

        with open(abs_path) as f:
            return json.load(f)


    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "aws_group_config.json"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        group_name = jdict.get('group-name')
        init_time = LocalizedDatetime.construct_from_iso8601(jdict.get('time-initiated'))
        ml = jdict.get('ml')
        unix_group = jdict.get('unix-group')

        if isinstance(ml, bool):
            ml = 'vB.1' if ml else 'm0'

        return cls(group_name, init_time, unix_group=unix_group, ml=ml)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, group_name, init_time, unix_group=None, ml='m0'):
        """
        Constructor
        """
        super().__init__()

        if unix_group is None:
            try:
                group_info = grp.getgrnam('ggc_user')
                unix_group = group_info[2]
            except KeyError:
                raise KeyError('GGC_USER')

        self.__group_name = group_name                  # string
        self.__init_time = init_time                    # LocalisedDatetime
        self.__unix_group = unix_group                  # int
        self.__ml = ml                                  # string (was bool)


    def __eq__(self, other):
        try:
            return self.group_name == other.group_name and self.init_time == other.init_time and \
                   self.unix_group == other.unix_group and self.ml == other.ml

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager, encryption_key=None):
        if self.__init_time is None:
            self.__init_time = LocalizedDatetime.now()

        super().save(manager, encryption_key=encryption_key)


    # ----------------------------------------------------------------------------------------------------------------

    def configurator(self, client):
        return AWSGroupConfigurator(self, client)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['group-name'] = self.group_name
        jdict["time-initiated"] = self.init_time
        jdict['unix-group'] = self.unix_group
        jdict['ml'] = self.ml

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def group_name(self):
        return self.__group_name


    @property
    def init_time(self):
        return self.__init_time


    @property
    def unix_group(self):
        return self.__unix_group


    @property
    def ml(self):
        return self.__ml


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AWSGroupConfiguration:{group_name:%s, init_time:%s, unix_group:%s, ml:%s}" % \
               (self.group_name, self.init_time, self.unix_group, self.ml)


# --------------------------------------------------------------------------------------------------------------------

class AWSGroupConfigurator(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, config: AWSGroupConfiguration, client):
        """
        Constructor
        """
        self.__logger = Logging.getLogger()

        self.__config = config                      # AWSGroupConfiguration
        self.__client = client                      # Client
        self.__aws_info = PathDict()                # PathDict


    # ----------------------------------------------------------------------------------------------------------------

    def collect_information(self, host):
        aws_json_reader = AWSGroup(self.config.group_name, self.__client)
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
        r_data = AWSGroupConfiguration.read(self.config.ml, 'gg_resources.json')

        # Edit JSON for device
        system_id = str(self.__aws_info.node("SystemID"))
        temp = host.home_path()
        group_owner_name = temp.split("/")[2]
        scs_path = host.scs_path()
        r_data["Name"] = ("Resources-" + system_id)
        r_data_resources = r_data["InitialVersion"]["Resources"]

        r_data_resources[0]["Id"] = (system_id + "-data-volume")
        r_data_resources[0]["ResourceDataContainer"]["LocalVolumeResourceData"][
            "GroupOwnerSetting"]["AutoAddGroupOwner"] = False
        r_data_resources[0]["ResourceDataContainer"]["LocalVolumeResourceData"][
            "SourcePath"] = scs_path
        r_data_resources[0]["ResourceDataContainer"]["LocalVolumeResourceData"][
            "GroupOwnerSetting"]["GroupOwner"] = group_owner_name

        if self.config.ml:
            r_data_resources[1]["Id"] = (system_id + "-ml-pm1")
            r_data_resources[2]["Id"] = (system_id + "-ml-pm2p5")
            r_data_resources[3]["Id"] = (system_id + "-ml-pm10")

            try:
                r_data_resources[4]["Id"] = (system_id + "-ml-no2")
            except IndexError:
                pass

            try:
                r_data_resources[5]["Id"] = (system_id + "-ml-no")
            except IndexError:
                pass

            try:
                r_data_resources[6]["Id"] = (system_id + "-ml-o3")
            except IndexError:
                pass

            try:
                r_data_resources[7]["Id"] = (system_id + "-ml-so2")
            except IndexError:
                pass

        # Send request
        self.__logger.info("Creating resource definition")
        self.__logger.info(r_data)

        response = self.__client.create_resource_definition(InitialVersion=r_data["InitialVersion"])
        self.__aws_info.append("NewResourceARN", response["LatestVersionArn"])

        self.__logger.info(response)


    # ----------------------------------------------------------------------------------------------------------------

    def define_aws_group_functions(self):
        # Get template JSON
        f_data = AWSGroupConfiguration.read(self.config.ml, 'gg_functions.json')

        # Update JSON for device
        system_id = str(self.__aws_info.node("SystemID"))
        data_volume_name = (system_id + "-data-volume")
        f_data_functions = f_data["InitialVersion"]["Functions"]

        f_data_functions[0]["Id"] = (system_id + "-ControlSubscriber")
        f_data_functions[1]["Id"] = (system_id + "-TopicPublisher")

        f_data_functions[0]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][0][
            "ResourceId"] = data_volume_name
        f_data_functions[1]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][0][
            "ResourceId"] = data_volume_name

        if self.config.ml:
            f_data_functions[2]["Id"] = (system_id + "-PMxInference")
            f_data_functions[2]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][
                0]["ResourceId"] = data_volume_name
            f_data_functions[2]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][
                1]["ResourceId"] = (system_id + "-ml-pm1")
            f_data_functions[2]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][
                2]["ResourceId"] = (system_id + "-ml-pm2p5")
            f_data_functions[2]["FunctionConfiguration"]["Environment"]["ResourceAccessPolicies"][
                3]["ResourceId"] = (system_id + "-ml-pm10")

            try:
                f_data_functions[3]["Id"] = (system_id + "-GasInference")
            except IndexError:
                pass

            try:
                f_data_functions[3]["FunctionConfiguration"]["Environment"][
                    "ResourceAccessPolicies"][0]["ResourceId"] = data_volume_name
            except IndexError:
                pass

            try:
                f_data_functions[3]["FunctionConfiguration"]["Environment"][
                    "ResourceAccessPolicies"][1]["ResourceId"] = (system_id + "-ml-no2")
            except IndexError:
                pass

            try:
                f_data_functions[3]["FunctionConfiguration"]["Environment"][
                    "ResourceAccessPolicies"][2]["ResourceId"] = (system_id + "-ml-no")
            except IndexError:
                pass

            try:
                f_data_functions[3]["FunctionConfiguration"]["Environment"][
                    "ResourceAccessPolicies"][3]["ResourceId"] = (system_id + "-ml-o3")
            except IndexError:
                pass

            try:
                f_data_functions[3]["FunctionConfiguration"]["Environment"][
                    "ResourceAccessPolicies"][4]["ResourceId"] = (system_id + "-ml-so2")
            except IndexError:
                pass

        self.__logger.info("Creating function definition")
        self.__logger.info(f_data)

        # Create request
        response = self.__client.create_function_definition(InitialVersion=f_data["InitialVersion"])
        self.__aws_info.append("NewFunctionARN", response["LatestVersionArn"])

        self.__logger.info(response)


    # ----------------------------------------------------------------------------------------------------------------

    def define_aws_group_subscriptions(self):
        s_data = AWSGroupConfiguration.read('m0', 'gg_subscriptions.json')

        # Edit for device
        system_id = str(self.__aws_info.node("SystemID"))
        s_data_subs = s_data["InitialVersion"]["Subscriptions"]
        s_data_subs[0]["Id"] = (system_id + "-particulates-subscription")
        s_data_subs[1]["Id"] = (system_id + "-control-from-cloud-subscription")
        s_data_subs[2]["Id"] = (system_id + "-climate-subscription")
        s_data_subs[3]["Id"] = (system_id + "-status-subscription")
        s_data_subs[4]["Id"] = (system_id + "-control-to-cloud-subscription")
        s_data_subs[5]["Id"] = (system_id + "-gases-subscription")

        s_data_subs[0]["Subject"] = (self.__aws_info.node("LocationPath") + "/particulates")
        s_data_subs[1]["Subject"] = (self.__aws_info.node("DevicePath") + "/control")
        s_data_subs[2]["Subject"] = (self.__aws_info.node("LocationPath") + "/climate")
        s_data_subs[3]["Subject"] = (self.__aws_info.node("DevicePath") + "/status")
        s_data_subs[4]["Subject"] = (self.__aws_info.node("DevicePath") + "/control")
        s_data_subs[5]["Subject"] = (self.__aws_info.node("LocationPath") + "/gases")

        self.__logger.info("Creating sub definition")
        self.__logger.info(s_data)

        # Send request
        response = self.__client.create_subscription_definition(InitialVersion=s_data["InitialVersion"])
        self.__aws_info.append("NewSubscriptionARN", response["LatestVersionArn"])

        self.__logger.info(response)


    def define_aws_logger(self):
        l_data = AWSGroupConfiguration.read('m0', 'gg_logger.json')

        system_id = str(self.__aws_info.node("SystemID"))
        l_data["InitialVersion"]["Loggers"][0]["Id"] = (system_id + "-lambda-logger")

        self.__logger.info("Creating logger definition")
        self.__logger.info(l_data)

        response = self.__client.create_logger_definition(InitialVersion=l_data["InitialVersion"])
        self.__aws_info.append("NewLoggerARN", response["LatestVersionArn"])

        self.__logger.info(response)


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

    @property
    def config(self):
        return self.__config


    @property
    def client(self):
        return self.__client


    @property
    def aws_info(self):
        return self.__aws_info


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AWSGroupConfigurator:{config:%s, client:%s, aws_info:%s}" % \
               (self.config, self.client, self.aws_info)
