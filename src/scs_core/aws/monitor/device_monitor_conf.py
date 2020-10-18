"""
Created on 30 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import ast

from collections import OrderedDict

from scs_core.aws.manager.s3_manager import S3Manager
from scs_core.aws.monitor.device_monitor import DeviceMonitor


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitorConf(object):
    __FILENAME = "device_monitor_conf.json"
    __BUCKET_NAME = "scs-device-monitor"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        aws_region = jdict.get('aws-region')
        unresponsive_minutes_allowed = jdict.get('unresponsive-minutes-allowed')
        bucket_name = jdict.get('bucket-name')
        resource_name = jdict.get('resource-name')

        return DeviceMonitorConf(aws_region, unresponsive_minutes_allowed, bucket_name, resource_name)

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, aws_region=None, unresponsive_minutes_allowed=None, bucket_name=None, resource_name=None):
        """
        Constructor
        """
        self.__aws_region = aws_region
        self.__unresponsive_minutes_allowed = unresponsive_minutes_allowed
        self.__bucket_name = bucket_name
        self.__resource_name = resource_name

    # ----------------------------------------------------------------------------------------------------------------

    def init_device_manager(self, host, email_client):
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

    def load_from_cloud(self, client, resource_client):
        # This should be the only way to init - how check?
        file_manager = S3Manager(client, resource_client)
        res = file_manager.retrieve_from_bucket(self.__BUCKET_NAME, self.__FILENAME)
        dev_list = ast.literal_eval(res)
        jdict = OrderedDict(dev_list)
        return self.construct_from_jdict(jdict)

    def save_to_cloud(self, client):
        to_save = str(self.as_json())
        to_save = to_save.replace("OrderedDict", " ")
        to_save = to_save.replace("[", " ")
        to_save = to_save.replace("]", " ")
        to_save = to_save.replace(" ", "")
        to_save = to_save[1:]
        to_save = to_save[0:-1]
        to_save = to_save.replace("\'", "\"")
        to_save_bytes = bytes(to_save, 'utf-8')
        client.put_object(Body=to_save_bytes, Bucket=self.__BUCKET_NAME, Key=self.__FILENAME)
        return to_save

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceManagerConf:{aws_region:%s, unresponsive_minutes_allowed:%s, " \
               "bucket_name:%s, resource_name:%s}" %\
               (DeviceMonitorConf.aws_region, DeviceMonitorConf.unresponsive_minutes_allowed,
                DeviceMonitorConf.bucket_name, DeviceMonitorConf.resource_name)
