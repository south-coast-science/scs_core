"""
Created on 29 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

the I2C addresses of the internal (in A4 pot) and external (exposed to air) SHTs


"""
from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------
class DeviceLine(PersistentJSONable):
    __FILENAME = "device_list.json"

    @classmethod
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device_tag = jdict.get('dev-tag')
        email_list = jdict.get('email')
        status_active = jdict.get("status")
        last_status_change = jdict.get("last_status_change")
        last_checked = jdict.get("last_checked")

        return DeviceLine(device_tag, email_list, status_active, last_status_change, last_checked)

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_tag, email_list, status_active, last_status_change, last_checked):
        """
        Constructor
        """
        self.__dm_status = ""  # for device monitor use only
        self.__device_tag = device_tag
        self.__email_list = email_list
        self.__status_active = status_active
        self.__last_status_change = last_status_change
        self.__last_checked = last_checked

    # ----------------------------------------------------------------------------------------------------------------
    @property
    def device_tag(self):
        return self.__device_tag

    @property
    def email_list(self):
        return self.__email_list

    @property
    def status_active(self):
        return self.__status_active

    @property
    def last_status_change(self):
        return self.__last_status_change

    @property
    def last_checked(self):
        return self.__last_checked

    @property
    def dm_status(self):
        return self.__dm_status

    @dm_status.setter
    def dm_status(self, dm_status):
        self.__dm_status = dm_status

    @status_active.setter
    def status_active(self, status_active):
        self.__status_active = status_active



    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['dev-tag'] = self.__device_tag
        jdict['email'] = self.__email_list
        jdict["status-active"] = self.__status_active
        jdict["last-status-change"] = self.__last_status_change
        jdict["last-checked"] = self.__last_checked

        return jdict

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceLine:{dev-tag: %s, email: %s, status-active:%s, last-status-change:%s, last-check:%s}" % \
               (DeviceLine.device_tag, DeviceLine.email_list, DeviceLine.status_active, DeviceLine.last_status_change,
                DeviceLine.last_checked)
