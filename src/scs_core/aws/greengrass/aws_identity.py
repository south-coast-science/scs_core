"""
Created on 09 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import json
import os
import shutil

from collections import OrderedDict
from urllib.request import urlopen

from scs_core.aws.config.aws import AWS
from scs_core.data.json import PersistentJSONable
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class AWSIdentity(PersistentJSONable):
    """
    classdocs
    """

    __KEEP_ALIVE = 60               # seconds

    __CERTS_PATH = "/greengrass/certs/"
    __ATS_ROOT_CA_RSA_2048_REMOTE_LOCATION = "https://www.amazontrust.com/repository/AmazonRootCA1.pem"

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME = "greengrass_identity.json"

    @classmethod
    def persistence_location(cls):
        return cls.aws_dir(), cls.__FILENAME


    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if jdict is None:
            return None

        core_name = jdict.get('core-name')
        group_name = jdict.get('group-name')
        iot_client = None
        gg_client = None

        return AWSIdentity(iot_client, gg_client, core_name, group_name)


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def return_default_policy():
        # create iot policy

        core_policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    # iot data plane
                    "Action": ["iot:Publish", "iot:Subscribe", "iot:Connect", "iot:Receive", "iot:GetThingShadow",
                               "iot:DeleteThingShadow", "iot:UpdateThingShadow"],
                    "Resource": ["arn:aws:iot:us-west-2:*:*"]
                },
                {
                    "Effect": "Allow",
                    # Greengrass data plane
                    "Action": ["greengrass:AssumeRoleForGroup", "greengrass:CreateCertificate",
                               "greengrass:GetConnectivityInfo", "greengrass:GetDeployment",
                               "greengrass:GetDeploymentArtifacts", "greengrass:UpdateConnectivityInfo",
                               "greengrass:UpdateCoreDeploymentStatus"],
                    "Resource": ["*"]
                }
            ]
        }
        return core_policy_doc


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, iot_client, gg_client, core_name, group_name):
        """
        Constructor
        """
        super().__init__()

        self.__logger = Logging.getLogger()

        self.__iot_client = iot_client
        self.__gg_client = gg_client
        self.__core_name = core_name
        self.__group_name = group_name
        self.__thing_arn = None
        self.__thing_id = None
        self.__certificate = None
        self.__latest_core_version_arn = None
        self.__latest_logger_version_arn = None
        self.__latest_group_version_arn = None
        self.__hash = None


    def __eq__(self, other):
        try:
            return self.core_name == other.core_name and self.group_name == other.group_name

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def setup_device(self):
        self.create_logger()
        self.create_thing()
        self.create_core()
        self.create_group()
        self.persist_certs()
        self.update_config_file()


    # ----------------------------------------------------------------------------------------------------------------

    def create_thing(self):
        # Create core
        res = self.__iot_client.create_thing(thingName=self.__core_name)
        self.__thing_arn = res["thingArn"]
        self.__thing_id = res["thingId"]

        self.__logger.info("Core created")

        # Create certs
        self.__certificate = self.__iot_client.create_keys_and_certificate(setAsActive=True)

        self.__logger.info("Cert created")

        # Attach cert to core
        cert_arn = self.__certificate["certificateArn"]
        self.__iot_client.attach_thing_principal(
            thingName=self.__core_name,
            principal=cert_arn,
        )

        self.__logger.info("Cert attached to core")

        # Create policy
        policy_doc = self.return_default_policy()
        policy_name = "{}_basic_policy".format(self.__core_name)

        self.__iot_client.create_policy(
            policyName=policy_name,
            policyDocument=json.dumps(policy_doc)
        )

        self.__logger.info("Policy created")
        self.__logger.info(json.dumps(policy_doc))

        # Attach policy
        # associate iot policy with core cert
        self.__iot_client.attach_policy(
            policyName=policy_name,
            target=cert_arn,
        )

        self.__logger.info("Policy attached to cert")


    def create_core(self):
        initial_core_definition_version = {
            'Cores': [
                {
                    'Id': self.__core_name,
                    'CertificateArn': self.__certificate["certificateArn"],
                    'SyncShadow': False,
                    'ThingArn': self.__thing_arn,
                }
            ]
        }
        res = self.__gg_client.create_core_definition(
            Name="{}_def".format(self.__core_name),
            InitialVersion=initial_core_definition_version,
        )
        self.__latest_core_version_arn = res['LatestVersionArn']

        self.__logger.info("Core created")
        self.__logger.info(initial_core_definition_version)


    def create_group(self):
        initial_group_definition_version = {
            'CoreDefinitionVersionArn': self.__latest_core_version_arn,
            'LoggerDefinitionVersionArn': self.__latest_logger_version_arn,
        }

        res = self.__gg_client.create_group(
            InitialVersion=initial_group_definition_version,
            Name=self.__group_name,
        )
        self.__latest_group_version_arn = res['LatestVersionArn']

        self.__logger.info("Group definition created")
        self.__logger.info(initial_group_definition_version)


    def create_logger(self):
        res = self.__gg_client.create_logger_definition(
            InitialVersion={
                'Loggers': [
                    {
                        'Component': 'GreengrassSystem',
                        'Id': 'Logger_definition_to_greengrass_system_' + self.__group_name,
                        'Level': 'INFO',
                        'Space': 1280,
                        'Type': 'FileSystem',
                    },
                    {
                        'Component': 'Lambda',
                        'Id': 'Logger_definition_to_lambda_' + self.__group_name,
                        'Level': 'INFO',
                        'Space': 1280,
                        'Type': 'FileSystem',
                    },
                ]
            },
            Name='Logger_definition_' + self.__group_name,
        )
        self.__latest_logger_version_arn = res['LatestVersionArn']

        self.__logger.info("Logger created")


    def persist_certs(self):
        # Delete existing keys from dir
        # Add new keys
        keys = self.__certificate["keyPair"]
        self.__hash = self.__certificate["certificateId"]
        self.__hash = self.__hash[0: 10]
        certificate_path = self.__hash + ".cert.pem"
        private_path = self.__hash + ".private.key"
        public_path = self.__hash + ".public.key"

        certs_dir = self.__CERTS_PATH
        if os.path.isdir(certs_dir):
            shutil.rmtree(certs_dir)  # remove dir and all contains
            self.__logger.info("Removed old keys")

        os.mkdir(certs_dir)

        data = urlopen(url=self.__ATS_ROOT_CA_RSA_2048_REMOTE_LOCATION)
        with open(certs_dir + "root.ca.pem", "wb") as local_file:
            local_file.write(data.read())

        f = open(certs_dir + "/" + certificate_path, "w")
        f.write(self.__certificate["certificatePem"])
        f.close()

        self.__logger.info("Cert saved")

        f = open(certs_dir + "/" + private_path, "w")
        f.write(keys["PrivateKey"])
        f.close()

        self.__logger.info("Private key saved")

        f = open(certs_dir + "/" + public_path, "w")
        f.write(keys["PublicKey"])
        f.close()

        self.__logger.info("Public key saved")


    def update_config_file(self):
        res = self.__iot_client.describe_endpoint(
            endpointType='iot:Data-ATS'
        )
        endpoint = res["endpointAddress"]
        config_dir = "/greengrass/config"
        if os.path.isdir(config_dir):
            shutil.rmtree(config_dir)  # remove dir and all contains
            self.__logger.info("Removed old config")

        os.mkdir(config_dir)
        default_config = {
            "coreThing": {
                "caPath": "root.ca.pem",
                "certPath": "%s.cert.pem" % self.__hash,
                "keyPath": "%s.private.key" % self.__hash,
                "thingArn": self.__thing_arn,
                "iotHost": endpoint,
                "ggHost": "greengrass-ats.iot.%s.amazonaws.com" % AWS.region(),
                "keepAlive": self.__KEEP_ALIVE,
                "ggDaemonPort": 8000,
                "systemComponentAuthTimeout": 5000
            },
            "runtime": {
                "maxWorkItemCount": 1024,
                "cgroup": {
                    "useSystemd": "yes"
                }
            },
            "managedRespawn": "false",
            "crypto": {
                "principals": {
                    "SecretsManager": {
                        "privateKeyPath": "file:///greengrass/certs/%s.private.key" % self.__hash
                    },
                    "IoTCertificate": {
                        "privateKeyPath": "file:///greengrass/certs/%s.private.key" % self.__hash,
                        "certificatePath": "file:///greengrass/certs/%s.cert.pem" % self.__hash
                    }
                },
                "caPath": "file:///greengrass/certs/root.ca.pem"
            }
        }

        f = open(config_dir + "/config.json", "w")
        f.write(json.dumps(default_config))
        f.close()

        self.__logger.info("Config saved")
        self.__logger.info(json.dumps(default_config))


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, *args, **kwargs):
        jdict = OrderedDict()

        jdict['core-name'] = self.core_name
        jdict['group-name'] = self.group_name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def core_name(self):
        return self.__core_name


    @property
    def group_name(self):
        return self.__group_name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AWSIdentity:{core_name:%s, group_name:%s}" % (self.core_name, self.group_name)

