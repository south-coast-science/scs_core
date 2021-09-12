"""
Created on 21 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"mode": "SYS", "device-name": "SCS Praxis/Handheld (dev)", "startup-message": "ON", "shutdown-message": "STANDBY",
"show-time": true}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable


# --------------------------------------------------------------------------------------------------------------------

class DisplayConf(PersistentJSONable):
    """
    classdocs
    """

    __MODES = ['SYS']

    @classmethod
    def modes(cls):
        return cls.__MODES


    __FILENAME = "system_display_conf.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        mode = jdict.get('mode')

        device_name = jdict.get('device-name')
        startup_message = jdict.get('startup-message')
        shutdown_message = jdict.get('shutdown-message')

        show_time = jdict.get('show-time', True)

        return cls(mode, device_name, startup_message, shutdown_message, show_time)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mode, device_name, startup_message, shutdown_message, show_time):
        """
        Constructor
        """
        super().__init__()

        self.__mode = mode                                          # string

        self.__device_name = device_name                            # string
        self.__startup_message = startup_message                    # string
        self.__shutdown_message = shutdown_message                  # string

        self.__show_time = show_time                                # bool


    def __eq__(self, other):
        try:
            return self.mode == other.mode and \
                   self.device_name == other.device_name and \
                   self.startup_message == other.startup_message and \
                   self.shutdown_message == other.shutdown_message and \
                   self.show_time == other.show_time

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mode(self):
        return self.__mode


    @property
    def device_name(self):
        return self.__device_name


    @property
    def startup_message(self):
        return self.__startup_message


    @property
    def shutdown_message(self):
        return self.__shutdown_message


    @property
    def show_time(self):
        return self.__show_time


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['mode'] = self.mode

        jdict['device-name'] = self.device_name
        jdict['startup-message'] = self.startup_message
        jdict['shutdown-message'] = self.shutdown_message

        jdict['show-time'] = self.show_time

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DisplayConf(core):{mode:%s, device_name:%s, startup_message:%s, shutdown_message:%s, " \
               "show_time:%s}" %  \
               (self.mode, self.device_name, self.startup_message, self.shutdown_message,
                self.show_time)
