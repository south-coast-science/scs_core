"""
Created on 25 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import json
import os
import time
from collections import OrderedDict
import logging

from botocore.exceptions import ClientError

from scs_core.aws.data.byline import TopicBylineGroup
from scs_core.aws.manager.s3_manager import S3Manager
from scs_core.aws.monitor.device_tester import DeviceTester
from scs_core.aws.monitor.scs_device import SCSDevice

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.timedelta import Timedelta


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitor(object):
    __RUN_FREQUENCY_MINUTES = 60
    __BUCKET_NAME = "scs-device-monitor"
    __RESOURCE_NAME_STATUS = "device_status_list"
    __RESOURCE_NAME_UPTIME = "device_uptime_list"
    __RESOURCE_NAME_BYLINES = "device_bylines_list"

    # ----------------------------------------------------------------------------------------------------------------
    def __init__(self, device_monitor_conf, client, resource_client, email_client, lambda_client):
        """
        Constructor
        """
        self.__config = device_monitor_conf
        self.__lambda_client = lambda_client
        self.__client = client
        self.__resource_client = resource_client
        self.__email_client = email_client

        logging.getLogger().setLevel(logging.INFO)

    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        # Get resources
        s3_manager = S3Manager(self.__client, self.__resource_client)
        device_statuses = s3_manager.retrieve_from_bucket(self.__BUCKET_NAME, self.__RESOURCE_NAME_STATUS)
        device_uptimes = s3_manager.retrieve_from_bucket(self.__BUCKET_NAME, self.__RESOURCE_NAME_UPTIME)
        device_byline_statuses = s3_manager.retrieve_from_bucket(self.__BUCKET_NAME, self.__RESOURCE_NAME_BYLINES)

        device_list = self.get_devices_by_byline()

        # Do all tests
        iterating = 0
        while iterating < len(device_list):
            this_dev = device_list[iterating]
            logging.info('Testing Device %s of %s: %s' % (iterating, len(device_list), this_dev.device_tag))

            self.get_latest_pubs(this_dev)

            device_tester = DeviceTester(this_dev, self.__config)
            # Check if device has stopped/started reporting
            if device_tester.is_inactive():
                this_dev.is_active = False
                logging.info('Device %s is inactive' % this_dev.device_tag)
            else:
                this_dev.is_active = True
                logging.info('Device %s is active' % this_dev.device_tag)
            if device_tester.has_status_changed(device_statuses):
                logging.info('Device %s has changed status' % this_dev.device_tag)
                this_dev.dm_status = "activity_change"
                self.generate_email(this_dev)
                this_dev.email_sent = True

            # see if all topics are published on recently
            device_tester.get_byline_activity()
            if not this_dev.email_sent:
                inactive, topic = device_tester.has_byline_status_changed(device_byline_statuses)
                if inactive:
                    logging.info('Device %s: ByLine %s: has become inactive. ' % (this_dev.device_tag, topic))
                    this_dev.dm_status = "byline"
                    self.generate_email(this_dev, topic)
                    this_dev.email_sent = True

            # check for weird (null) values
            if not this_dev.email_sent:
                is_okay, field, field_type = device_tester.check_values()
                this_dev.dm_status = "values"
                if not is_okay:
                    logging.info('Device %s: Field %s: has error values. ' % (this_dev.device_tag, field))
                    self.generate_email(this_dev, None, field, field_type)
                    this_dev.email_sent = True

            # check if rebooted
            if device_tester.was_rebooted(device_uptimes):
                this_dev.dm_status = "reboot"
                if not this_dev.email_sent:
                    logging.info('Device %s: May have been rebooted. ' % this_dev.device_tag)
                    self.generate_email(this_dev)
                    this_dev.email_sent = True

            iterating += 1

        self.recreate_status_list(device_list)
        self.recreate_uptime_list(device_list)
        self.recreate_pub_list(device_list)

    def send_email_alert(self, this_dev, message):
        # TODO allow for extra recipients
        try:
            self.__email_client.send_email(
                Source=self.__config.email_name,
                Destination={
                    'ToAddresses': [
                        self.__config.email_name
                    ]
                },
                Message={
                    'Subject': {
                        'Data': this_dev.device_tag
                    },
                    'Body': {
                        'Text': {
                            'Data': message
                        }
                    }
                }
            )
        except ClientError as e:
            logging.error("Received error: %s", e, exc_info=True)
            if e.response['Error']['Code'] == 'MessageRejected':
                pass
            else:
                raise
        logging.info("Email sent about device %s", this_dev.device_tag)
        time.sleep(1)  # AWS limit is 1 email/sec

    def get_devices_by_byline(self):
        device_list = []

        logging.info('Getting device topics response...')
        response = self.__lambda_client.invoke(
            FunctionName="arn:aws:lambda:us-west-2:696437392763:function:deviceTopics",
            InvocationType='RequestResponse',
        )

        logging.info('Received device topics response...')
        pl = response.get("Payload")
        data = pl.read()
        data.decode()
        json_data = json.loads(data)
        body = json_data.get("body")
        group = TopicBylineGroup.construct_from_jdict(body, excluded="/control")
        for device in group.devices:
            device_bylines = group.bylines_for_device(device)
            temp = SCSDevice(device, None, False, device_bylines)
            device_list.append(temp)
        return device_list

    def generate_email(self, device, byline_topic=None, field_name=None, field_type=None):
        template = None
        old_status = "inactive" if device.is_active else "active"
        now_status = "active" if device.is_active else "inactive"

        # Get templates
        if device.dm_status == "activity_change":
            template = "status_changed.txt"
        elif device.dm_status == "byline":
            template = "byline_inactive.txt"
        elif device.dm_status == "reboot":
            template = "uptime.txt"
        elif device.dm_status == "values":
            template = "values.txt"

        # Load template
        if template:
            filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'email_templates', template)
            f = open(filepath, "r")
            message = f.read()
        else:
            return

        # Replace for specific device
        message = (message.replace("DEVICE_NAME", device.device_tag))
        message = (message.replace("LAST_CHECK_TIME", self.get_last_run_time()))
        message = (message.replace("OLD_STATUS", old_status))
        message = (message.replace("NEW_STATUS", now_status))
        message = (message.replace("THIS_CHECK_TIME", str(LocalizedDatetime.now().datetime)))
        message = (message.replace("TOPIC_NAME", byline_topic if byline_topic else ""))
        message = (message.replace("TIME_ALLOWED", str(self.__config.unresponsive_minutes_allowed)))
        message = (message.replace("NOW_UPTIME", device.uptime if device.uptime else ""))
        message = (message.replace("OLD_UPTIME", device.old_uptime if device.old_uptime else ""))
        message = (message.replace("FIELD_NAME", field_name if field_name else ""))
        message = (message.replace("FIELD_TYPE", field_type if field_type else ""))
        self.send_email_alert(device, message)

    def get_last_run_time(self):
        now = LocalizedDatetime.now()
        td = Timedelta(minutes=self.__RUN_FREQUENCY_MINUTES)
        res = now - td
        return res.as_json()

    def recreate_status_list(self, device_list):
        s3_manager = S3Manager(self.__client, self.__resource_client)
        json_data = OrderedDict()
        for device in device_list:
            json_data[device.device_tag] = device.is_active
        data_string = json.dumps(json_data)
        data_string.encode()
        s3_manager.upload_bytes_to_bucket(data_string, self.__BUCKET_NAME, self.__RESOURCE_NAME_STATUS)
        logging.info('Uploaded new status list to s3')

    def recreate_uptime_list(self, device_list):
        s3_manager = S3Manager(self.__client, self.__resource_client)
        json_data = OrderedDict()
        for device in device_list:
            data = (device.as_uptime_json())
            json_data[data["dev-tag"]] = data["uptime"]
        data_string = json.dumps(json_data)
        data_string.encode()
        s3_manager.upload_bytes_to_bucket(data_string, self.__BUCKET_NAME, self.__RESOURCE_NAME_UPTIME)
        logging.info('Uploaded new uptime list to s3')

    def recreate_pub_list(self, device_list):
        s3_manager = S3Manager(self.__client, self.__resource_client)
        json_data = OrderedDict()
        for device in device_list:
            json_data[device.device_tag] = device.byline_status
        data_string = json.dumps(json_data)
        data_string.encode()
        s3_manager.upload_bytes_to_bucket(data_string, self.__BUCKET_NAME, self.__RESOURCE_NAME_BYLINES)
        logging.info('Uploaded new pub list to s3')

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_latest_pubs(scs_device):
        values = False
        device_bylines = scs_device.bylines
        for byline in device_bylines:
            if byline.pub is not None:
                values = True
        if values:
            latest = max([device_bylines.pub for device_bylines in device_bylines if device_bylines.pub is not None])
        else:
            latest = None
        scs_device.latest_pub = latest

    # ----------------------------------------------------------------------------------------------------------------
    def __str__(self, *args, **kwargs):
        return "DeviceMonitor:{config:%s}" % \
               self.__config
