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
            return cls(None, None, None)

        email_name = jdict.get('email-name')
        unresponsive_minutes_allowed = jdict.get('unresponsive-minutes-allowed')
        email_password = jdict.get('email-password')

        return cls(email_name, unresponsive_minutes_allowed, email_password)

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, email_name, unresponsive_minutes_allowed, email_password):
        """
        Constructor
        """
        self.__email_name = email_name
        self.__unresponsive_minutes_allowed = unresponsive_minutes_allowed
        self.__email_password = email_password

    # ----------------------------------------------------------------------------------------------------------------

    def create_device_monitor(self, persistence_manager, email_client, host=None):
        return DeviceMonitor(self, persistence_manager, email_client, host)

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def email_name(self):
        return self.__email_name

    @property
    def unresponsive_minutes_allowed(self):
        return self.__unresponsive_minutes_allowed

    @property
    def email_password(self):
        return self.__email_password

    # ----------------------------------------------------------------------------------------------------------------

    @email_name.setter
    def email_name(self, value):
        self.__email_name = value

    @unresponsive_minutes_allowed.setter
    def unresponsive_minutes_allowed(self, value):
        self.__unresponsive_minutes_allowed = value

    @email_password.setter
    def email_password(self, value):
        self.__email_password = value

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['email-password'] = self.email_password
        jdict['unresponsive-minutes-allowed'] = self.unresponsive_minutes_allowed
        jdict['email-name'] = self.email_name

        return jdict

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceManagerConf:{email_name:%s, unresponsive_minutes_allowed:%s, email_password:%s}" % \
               (DeviceMonitorConf.email_name, DeviceMonitorConf.unresponsive_minutes_allowed,
                DeviceMonitorConf.email_password)
