"""
Created on 25 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import json
import os
import logging

from collections import OrderedDict

from botocore.exceptions import ClientError

from scs_core.aws.data.byline import TopicBylineGroup
from scs_core.aws.data.email_list import EmailList

from scs_core.aws.monitor.device_tester import DeviceTester
from scs_core.aws.monitor.scs_device import SCSDevice

from scs_core.data.datetime import LocalizedDatetime

from scs_core.aws.data.runtime_record import RuntimeRecord
from scs_core.aws.data.uptime_list import UptimeList
from scs_core.aws.data.byline_list import BylineList
from scs_core.aws.data.activity_list import StatusList


# --------------------------------------------------------------------------------------------------------------------

class DeviceMonitor(object):


    # ----------------------------------------------------------------------------------------------------------------
    def __init__(self, device_monitor_conf, persistence_manager, email_client, lambda_client):
        """
        Constructor
        """
        self.__config = device_monitor_conf
        self.__lambda_client = lambda_client
        self.__persistence_manager = persistence_manager
        self.__email_client = email_client
        self.__runtime_record = None
        self.__email_list = EmailList.load(persistence_manager).as_json()

        logging.getLogger().setLevel(logging.INFO)

    # ----------------------------------------------------------------------------------------------------------------

    def run(self):
        # Get resources

        status_list = StatusList.load(self.__persistence_manager)
        uptime_list = UptimeList.load(self.__persistence_manager)
        byline_list = BylineList.load(self.__persistence_manager)
        self.__runtime_record = RuntimeRecord.load(self.__persistence_manager)

        device_status_list = status_list.as_json().get("status_list")
        device_uptime_list = uptime_list.as_json().get("uptime_list")
        device_byline_list = byline_list.as_json().get("byline_list")

        device_list = self.get_devices_by_byline()

        # Do all tests
        iterating = 0
        while iterating < len(device_list):
            this_dev = device_list[iterating]
            logging.debug('Testing Device %s of %s: %s' % (iterating, len(device_list), this_dev.device_tag))

            self.get_latest_pubs(this_dev)

            device_tester = DeviceTester(this_dev, self.__config)
            # Check if device has stopped/started reporting
            if device_tester.is_inactive():
                this_dev.is_active = False
                logging.debug('Device %s is inactive' % this_dev.device_tag)
            else:
                this_dev.is_active = True
                logging.debug('Device %s is active' % this_dev.device_tag)
            if device_tester.has_status_changed(device_status_list):
                logging.info('Device %s has changed status' % this_dev.device_tag)
                this_dev.dm_status = "activity_change"
                self.generate_email(this_dev)
                this_dev.email_sent = True

            # see if all topics are published on recently
            device_tester.get_byline_activity()
            if not this_dev.email_sent and this_dev.is_active:
                inactive, topic = device_tester.has_byline_status_changed(device_byline_list)
                if inactive:
                    logging.info('Device %s: ByLine %s: has become inactive. ' % (this_dev.device_tag, topic))
                    this_dev.dm_status = "byline"
                    self.generate_email(this_dev, topic)
                    this_dev.email_sent = True

            # check for weird (null) values
            if not this_dev.email_sent and this_dev.is_active:
                is_okay, topic, byline = device_tester.check_values()
                this_dev.dm_status = "values"
                if not is_okay:
                    logging.info('Device %s: Byline %s: has error values. ' % (this_dev.device_tag, topic))
                    self.generate_email(this_dev, topic, byline)
                    this_dev.email_sent = True

            # check if rebooted
            if this_dev.is_active:
                if device_tester.was_rebooted(device_uptime_list):
                    this_dev.dm_status = "reboot"
                    if not this_dev.email_sent:
                        logging.info('Device %s: May have been rebooted. ' % this_dev.device_tag)
                        self.generate_email(this_dev)
                        this_dev.email_sent = True

            iterating += 1

        self.recreate_status_list(device_list)
        self.recreate_uptime_list(device_list)
        self.recreate_pub_list(device_list)
        self.save_runtime_record()

    def send_email_alert(self, this_dev, text):
        jdict = self.__email_list.get("email_list")
        v_list = []
        for key, value in jdict.items():
            if key == this_dev.device_tag:
                if value is not None:
                    if type(value).__name__ == "list":
                        for item in value:
                            v_list.append(item)
                    else:
                        v_list.append(value)
                    break

        v_list.append(self.__config.email_name)
        v_list.append("bbeloff@me.com")
        message = text.split("~")
        subject = message[0]
        body = message[1]
        try:
            self.__email_client.send_email(
                Source=self.__config.email_name,
                Destination={
                    'ToAddresses': v_list
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        'Text': {
                            'Data': body
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
        # time.sleep(1)  # AWS limit is 1 email/sec

    def get_devices_by_byline(self):
        device_list = []

        logging.debug('Getting device topics response...')
        response = self.__lambda_client.invoke(
            FunctionName="arn:aws:lambda:us-west-2:696437392763:function:deviceTopics",
            InvocationType='RequestResponse',
        )

        logging.debug('Received device topics response...')
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

    def generate_email(self, device, byline_topic=None, document=None):
        template = None
        old_status = "offline" if device.is_active else "online"
        now_status = "online" if device.is_active else "offline"

        # Get templates
        if device.dm_status == "activity_change":
            if now_status == "offline":
                template = "status_offline.txt"
            else:
                template = "status_online.txt"
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
            logging.error("Template missing %s" % template)
            return
        # Replace for specific device
        last_runtime = self.__runtime_record.as_json() if self.__runtime_record else "Unknown"
        message = (message.replace("DEVICE_NAME", device.device_tag))
        message = (message.replace("LAST_CHECK_TIME", last_runtime.get("last_runtime")))
        message = (message.replace("OLD_STATUS", old_status))
        message = (message.replace("NEW_STATUS", now_status))
        message = (message.replace("THIS_CHECK_TIME", str(LocalizedDatetime.now().as_iso8601())))
        message = (message.replace("TOPIC_NAME", byline_topic if byline_topic else ""))
        message = (message.replace("TIME_ALLOWED", str(self.__config.unresponsive_minutes_allowed)))
        message = (message.replace("NOW_UPTIME", device.uptime if device.uptime else ""))
        message = (message.replace("OLD_UPTIME", device.old_uptime if device.old_uptime else ""))
        message = (message.replace("DOCUMENT", document.as_json if document else ""))
        self.send_email_alert(device, message)

    def recreate_status_list(self, device_list):
        device_data = OrderedDict()
        for device in device_list:
            device_data[device.device_tag] = device.is_active

        json_data = OrderedDict()
        json_data["status_list"] = device_data

        status_list = StatusList.construct_from_jdict(json_data)
        status_list.save(self.__persistence_manager)

        logging.debug('Uploaded new status list to s3')

    def recreate_uptime_list(self, device_list):
        device_data = OrderedDict()
        for device in device_list:
            data = (device.as_json())
            device_data[data["dev-tag"]] = data["uptime"]
        json_data = OrderedDict()
        json_data["uptime_list"] = device_data

        uptime_list = UptimeList.construct_from_jdict(json_data)
        uptime_list.save(self.__persistence_manager)
        logging.debug('Uploaded new uptime list to s3')

    def recreate_pub_list(self, device_list):
        device_data = OrderedDict()
        for device in device_list:
            device_data[device.device_tag] = device.byline_status
        json_data = OrderedDict()
        json_data["byline_list"] = device_data

        byline_list = BylineList.construct_from_jdict(json_data)
        byline_list.save(self.__persistence_manager)
        logging.debug('Uploaded new pub list to s3')

    def save_runtime_record(self):
        now = LocalizedDatetime.now().as_json()
        jdict = OrderedDict()

        jdict['last_runtime'] = now
        new_runtime_record = RuntimeRecord.construct_from_jdict(jdict)
        new_runtime_record.save(self.__persistence_manager)

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
