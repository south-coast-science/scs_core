"""
Created on 21 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"mode": "SYS", "device-name": "SCS Praxis/Handheld v1.0", "startup-message": "STARTING", "shutdown-message": "STANDBY"}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable

from scs_display.monitor.system_monitor import SystemMonitor


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
    def persistence_location(cls, host):
        return host.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        mode = jdict.get('mode')

        device_name = jdict.get('device-name')
        startup_message = jdict.get('startup-message')
        shutdown_message = jdict.get('shutdown-message')

        return DisplayConf(mode, device_name, startup_message, shutdown_message)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mode, device_name, startup_message, shutdown_message):
        """
        Constructor
        """
        super().__init__()

        self.__mode = mode

        self.__device_name = device_name
        self.__startup_message = startup_message
        self.__shutdown_message = shutdown_message


    # ----------------------------------------------------------------------------------------------------------------

    def monitor(self, queue_report_filename, gps_report_filename):
        if self.mode == 'SYS':
            return SystemMonitor.construct(self.device_name, self.startup_message, self.shutdown_message,
                                           queue_report_filename, gps_report_filename)

        raise ValueError('unknown mode: %s' % self.mode)


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


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['mode'] = self.mode

        jdict['device-name'] = self.device_name
        jdict['startup-message'] = self.startup_message
        jdict['shutdown-message'] = self.shutdown_message

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DisplayConf:{mode:%s, device_name:%s, startup_message:%s, shutdown_message:%s}" %  \
               (self.mode, self.device_name, self.startup_message, self.shutdown_message)
