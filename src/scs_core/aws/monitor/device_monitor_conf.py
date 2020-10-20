"""
Created on 30 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.aws.monitor.device_monitor import DeviceMonitor

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorConf(PersistentJSONable):
    """
    classdocs
    """

    __FILENAME = "device_monitor_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        aws_region = jdict.get('aws-region')
        unresponsive_minutes_allowed = jdict.get('unresponsive-minutes-allowed')
        bucket_name = jdict.get('bucket-name')
        resource_name = jdict.get('resource-name')

        return cls(aws_region, unresponsive_minutes_allowed, bucket_name, resource_name)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, aws_region, unresponsive_minutes_allowed, bucket_name, resource_name):
        """
        Constructor
        """
        self.__aws_region = aws_region
        self.__unresponsive_minutes_allowed = unresponsive_minutes_allowed
        self.__bucket_name = bucket_name
        self.__resource_name = resource_name


    # ----------------------------------------------------------------------------------------------------------------

    def device_monitor(self, host, email_client):
        return DeviceMonitor(self, host, email_client)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def aws_region(self):
        return self.__aws_region


    @property
    def unresponsive_minutes_allowed(self):
        return self.__unresponsive_minutes_allowed


    @property
    def bucket_name(self):
        return self.__bucket_name


    @property
    def resource_name(self):
        return self.__resource_name


    # ----------------------------------------------------------------------------------------------------------------

    @aws_region.setter
    def aws_region(self, value):
        self.__aws_region = value


    @unresponsive_minutes_allowed.setter
    def unresponsive_minutes_allowed(self, value):
        self.__unresponsive_minutes_allowed = value


    @bucket_name.setter
    def bucket_name(self, value):
        self.__bucket_name = value


    @resource_name.setter
    def resource_name(self, value):
        self.__resource_name = value


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['aws-region'] = self.aws_region
        jdict['unresponsive-minutes-allowed'] = self.unresponsive_minutes_allowed
        jdict['bucket-name'] = self.bucket_name
        jdict['resource-name'] = self.resource_name

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceManagerConf:{aws_region:%s, unresponsive_minutes_allowed:%s, " \
               "bucket_name:%s, resource_name:%s}" %\
               (DeviceMonitorConf.aws_region, DeviceMonitorConf.unresponsive_minutes_allowed,
                DeviceMonitorConf.bucket_name, DeviceMonitorConf.resource_name)
