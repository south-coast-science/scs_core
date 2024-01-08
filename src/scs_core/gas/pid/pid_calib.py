"""
Created on 24 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

www.alphasense-technology.co.uk...
{"serial_number": null, "type": "DSI", "calibrated_on": "2024-01-01", "dispatched_on": null, "pt1000_v20": null,
"sn1": {"serial_number": "143351067", "sensor_type": "PIDH2", "pid_zero_mv": null, "pid_sensitivity_mv_ppm": 44.9,
"test-calib": {"sensitivity": 0.786, "calibrated-on": "2024-01-05T13:16:04Z"}}}
"""

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.datum import Datum
from scs_core.data.json import JSONable

from scs_core.gas.sensor_calib import SensorCalib


# --------------------------------------------------------------------------------------------------------------------

class PIDTestCalib(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        sensitivity = jdict.get('sensitivity')
        calibrated_on = LocalizedDatetime.construct_from_iso8601(jdict.get('calibrated-on'))

        return cls(sensitivity, calibrated_on)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensitivity, calibrated_on):
        """
        Constructor
        """
        self.__sensitivity = float(sensitivity)                 # ratio of actual / expected or None
        self.__calibrated_on = calibrated_on                    # LocalizedDatetime


    def __eq__(self, other):
        try:
            return self.sensitivity == other.sensitivity and self.calibrated_on == other.calibrated_on

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sensitivity'] = self.sensitivity
        jdict['calibrated-on'] = self.calibrated_on

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sensitivity(self):
        return self.__sensitivity


    @sensitivity.setter
    def sensitivity(self, sensitivity):
        self.__sensitivity = sensitivity


    @property
    def calibrated_on(self):
        return self.__calibrated_on


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TestCalib:{sensitivity:%s, calibrated_on:%s}" % \
                    (self.sensitivity, self.calibrated_on)


# --------------------------------------------------------------------------------------------------------------------

class PIDCalib(SensorCalib):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        serial_number = jdict.get('serial_number')
        sensor_type = jdict.get('sensor_type')

        if 'pid_zero_mv' in jdict:
            pid_elc_mv = jdict.get('pid_zero_mv')
        else:
            pid_elc_mv = jdict.get('we_sensor_zero_mv')

        if 'pid_sensitivity_mv_ppm' in jdict:
            pid_sens_mv_ppm = jdict.get('pid_sensitivity_mv_ppm')
        else:
            pid_sens_mv_ppm = jdict.get('we_sensitivity_mv_ppb')        # uses mV / ppb field to record mV / ppm

        bump_calib = PIDTestCalib.construct_from_jdict(jdict.get('bump-calib'))

        return cls(serial_number, sensor_type, pid_elc_mv, pid_sens_mv_ppm, bump_calib)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type, pid_elc_mv, pid_sens_mv_ppm, bump_calib):
        """
        Constructor
        """
        SensorCalib.__init__(self, serial_number, sensor_type)

        self.__pid_elc_mv = Datum.float(pid_elc_mv, 3)                  # PID electronic zero           mV
        self.__pid_sens_mv_ppm = Datum.float(pid_sens_mv_ppm, 6)        # PID sensitivity               mV / ppm
        self.__bump_calib = bump_calib                                  # PIDTestCalib

        self.validate()


    def __eq__(self, other):
        try:
            return self.serial_number == other.serial_number and self.sensor_type == other.sensor_type and \
                   self.pid_elc_mv == other.pid_elc_mv and self.pid_sens_mv_ppm == other.pid_sens_mv_ppm and  \
                   self.bump_calib == other.bump_calib

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def validate(self):
        if self.pid_sens_mv_ppm == 0.0:
            raise ValueError('%s - pid_sensitivity_mv_ppm: zero sensitivity' % self.sensor_type)


    # ----------------------------------------------------------------------------------------------------------------

    def set_defaults(self):
        pass                                # PID may have null values


    def set_sens_mv_from_sens_na(self):
        pass                                # sensitivity nA data is not available


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial_number'] = self.serial_number
        jdict['sensor_type'] = self.sensor_type

        jdict['pid_zero_mv'] = self.pid_elc_mv
        jdict['pid_sensitivity_mv_ppm'] = self.pid_sens_mv_ppm
        jdict['bump-calib'] = self.bump_calib

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pid_elc_mv(self):
        return self.__pid_elc_mv


    @property
    def pid_sens_v_ppb(self):
        return self.__pid_sens_mv_ppm / 1000000.0


    @property
    def pid_sens_mv_ppm(self):
        return self.__pid_sens_mv_ppm


    @property
    def bump_sensitivity(self):
        return None if self.__bump_calib is None else self.__bump_calib.sensitivity


    @property
    def bump_calib(self):
        return self.__bump_calib


    @bump_calib.setter
    def bump_calib(self, bump_calib):
        self.__bump_calib = bump_calib


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PIDCalib:{serial_number:%s, sensor_type:%s, pid_elc_mv:%s, pid_sens_mv_ppm:%s, bump_calib:%s}" % \
                    (self.serial_number, self.sensor_type, self.pid_elc_mv, self.pid_sens_mv_ppm, self.bump_calib)
