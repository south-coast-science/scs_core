"""
Created on 5 Jul 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Experimental updater for AWS IoT cloud definition of a group - not currently working (this may be impossible).
"""

from scs_core.aws.greengrass.v1.aws_group_version import AWSGroupVersion

from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class AWSIdentityUpdate(object):
    """
    classdocs
    """

    __LOG_LEVEL = 'WARN'
    __LOG_SPACE = 1280

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, iot_client, gg_client, group_version: AWSGroupVersion):
        """
        Constructor
        """
        super().__init__()

        self.__iot_client = iot_client
        self.__gg_client = gg_client
        self.__group_version = group_version

        self.__logger = Logging.getLogger()


    def __eq__(self, other):
        try:
            return self.core_name == other.core_name and self.group_name == other.group_name

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def update_device(self):
        logger_arn = self.create_logger()
        group_arn = self.create_group(logger_arn)

        return group_arn


    # ----------------------------------------------------------------------------------------------------------------

    def create_group(self, logger_arn):
        initial_group_definition_version = {
            'CoreDefinitionVersionArn': self.core_arn,
            'LoggerDefinitionVersionArn': logger_arn
        }

        self.__logger.info(initial_group_definition_version)

        res = self.__gg_client.create_group(
            InitialVersion=initial_group_definition_version,
            Name=self.group_name
        )

        self.__logger.info("group definition created")

        return res['LatestVersionArn']


    def create_logger(self):
        res = self.__gg_client.create_logger_definition(
            InitialVersion={
                'Loggers': [
                    {
                        'Component': 'GreengrassSystem',
                        'Id': 'Logger_definition_to_greengrass_system_' + self.group_name,
                        'Level': self.__LOG_LEVEL,
                        'Space': self.__LOG_SPACE,
                        'Type': 'FileSystem',
                    },
                    {
                        'Component': 'Lambda',
                        'Id': 'Logger_definition_to_lambda_' + self.group_name,
                        'Level': self.__LOG_LEVEL,
                        'Space': self.__LOG_SPACE,
                        'Type': 'FileSystem',
                    },
                ]
            },
            Name='Logger_definition_' + self.group_name
        )

        self.__logger.info("logger created")

        return res['LatestVersionArn']


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def core_name(self):
        return self.__group_version.core_name


    @property
    def group_name(self):
        return self.__group_version.group_name


    @property
    def core_arn(self):
        return self.__group_version.core_arn


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AWSIdentityUpdate:{core_name:%s, group_name:%s}" % (self.core_name, self.group_name)
