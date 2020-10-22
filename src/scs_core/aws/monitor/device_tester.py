"""
Created on 08 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import ast

from scs_core.data.timedelta import Timedelta

from scs_core.aws.manager.lambda_message_manager import MessageManager

from scs_core.data.datetime import LocalizedDatetime


class DeviceTester(object):
    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, scs_device, config, host):
        """
        Constructor
        """
        self.__scs_device = scs_device
        self.__config = config
        self.__host = host

    # ----------------------------------------------------------------------------------------------------------------

    def is_inactive(self):
        latest_pub = self.__scs_device.latest_pub

        if latest_pub is None:
            return True

        now = LocalizedDatetime.now()
        delta = now - latest_pub

        return delta.minutes > self.__config.unresponsive_minutes_allowed

    def is_byline_inactive(self, byline):
        latest_pub = byline.pub
        if latest_pub is None:
            return True
        else:
            now = LocalizedDatetime.now()
            delta = now - latest_pub
            return delta.minutes > self.__config.unresponsive_minutes_allowed

    def has_status_changed(self, s3_device_status_list):
        is_active = not self.is_inactive()
        old_device_status_list = ast.literal_eval(s3_device_status_list)
        was_active = old_device_status_list[self.__scs_device.device_tag]
        if bool(is_active) == bool(was_active):
            return False
        else:
            return True

    def is_publishing_on_all_channels(self):
        device_bylines = self.__scs_device.bylines
        for byline in device_bylines:
            if self.is_byline_inactive(byline):
                return True, byline
            return False, None

    def was_rebooted(self, s3_device_uptime_list):
        message_manager = MessageManager(self.__host)
        device_bylines = self.__scs_device.bylines

        old_device_uptime_list = ast.literal_eval(s3_device_uptime_list)
        old_period = Timedelta.construct_from_jdict(old_device_uptime_list[self.__scs_device.device_tag])

        for byline in device_bylines:
            if "status" in byline.topic:
                res = message_manager.find_latest_for_topic(byline.topic, LocalizedDatetime.now())
                if res is None:
                    # It doesn't have this channel for some reason
                    return False
                else:
                    json_response = res.as_json()
                    period = Timedelta().construct_from_jdict(json_response['payload']["val"]["up"]["period"])
                    if old_period is not None:
                        if period < old_period:
                            # device has been reset
                            self.__scs_device.uptime = period
                            return True
                        else:
                            # device has not been reset
                            self.__scs_device.uptime = period
                            return False
                    else:
                        # device does not have a pre-existing uptime - it is probably new
                        self.__scs_device.uptime = period
                        return False

    # ----------------------------------------------------------------------------------------------------------------
