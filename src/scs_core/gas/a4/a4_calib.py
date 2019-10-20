"""
Created on 24 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable

from scs_core.gas.sensor_calib import SensorCalib


# --------------------------------------------------------------------------------------------------------------------

class A4Calib(SensorCalib, JSONable):
    """
    classdocs
    """

    # used for Digital Single Interface...
    DEFAULT_WE_ELECTRONIC_ZERO_MV =     300
    DEFAULT_WE_SENSOR_ZERO_MV =           0
    DEFAULT_WE_TOTAL_ZERO_MV =          300

    DEFAULT_AE_ELECTRONIC_ZERO_MV =     300
    DEFAULT_AE_SENSOR_ZERO_MV =           0
    DEFAULT_AE_TOTAL_ZERO_MV =          300

    DEFAULT_PCB_GAIN =                  -0.7


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        serial_number = jdict.get('serial_number')
        sensor_type = jdict.get('sensor_type')

        we_elc_mv = jdict.get('we_electronic_zero_mv')
        we_cal_mv = jdict.get('we_sensor_zero_mv')
        we_tot_mv = jdict.get('we_total_zero_mv')

        ae_elc_mv = jdict.get('ae_electronic_zero_mv')
        ae_cal_mv = jdict.get('ae_sensor_zero_mv')
        ae_tot_mv = jdict.get('ae_total_zero_mv')

        we_sens_na = jdict.get('we_sensitivity_na_ppb')
        we_x_sens_na = jdict.get('we_cross_sensitivity_no2_na_ppb')

        pcb_gain = jdict.get('pcb_gain')

        we_sens_mv = jdict.get('we_sensitivity_mv_ppb')
        we_no2_x_sens_mv = jdict.get('we_cross_sensitivity_no2_mv_ppb')


        return A4Calib(serial_number, sensor_type, we_elc_mv, we_cal_mv, we_tot_mv, ae_elc_mv, ae_cal_mv, ae_tot_mv,
                       we_sens_na, we_x_sens_na, pcb_gain, we_sens_mv, we_no2_x_sens_mv)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, serial_number, sensor_type, we_elc_mv, we_cal_mv, we_tot_mv, ae_elc_mv, ae_cal_mv, ae_tot_mv,
                 we_sens_na, we_x_sens_na, pcb_gain, we_sens_mv, we_no2_x_sens_mv):
        """
        Constructor
        """
        SensorCalib.__init__(self, serial_number, sensor_type)

        self.__we_elc_mv = Datum.int(we_elc_mv)                     # WE electronic zero                    mV
        self.__we_cal_mv = Datum.int(we_cal_mv)                     # WE sensor zero at 23 °C               mV
        self.__we_tot_mv = Datum.int(we_tot_mv)                     # total WE zero                         mV

        self.__ae_elc_mv = Datum.int(ae_elc_mv)                     # Aux electronic zero                   mV
        self.__ae_cal_mv = Datum.int(ae_cal_mv)                     # Aux sensor zero at 23 °C              mV
        self.__ae_tot_mv = Datum.int(ae_tot_mv)                     # total Aux zero                        mV

        self.__we_sens_na = Datum.float(we_sens_na, 3)              # WE sensitivity                        nA
        self.__we_x_sens_na = Datum.float(we_x_sens_na, 3)          # WE cross-sensitivity                  nA

        self.__pcb_gain = Datum.float(pcb_gain, 3)                  # PCB gain                              mv / nA

        self.__we_sens_mv = Datum.float(we_sens_mv, 3)              # WE sensitivity                        mV / ppb
        self.__we_no2_x_sens_mv = Datum.float(we_no2_x_sens_mv, 3)  # WE cross-sensitivity                  mV / ppb


    # ----------------------------------------------------------------------------------------------------------------

    def set_defaults(self):
        self.__we_elc_mv = self.DEFAULT_WE_ELECTRONIC_ZERO_MV
        self.__we_cal_mv = self.DEFAULT_WE_SENSOR_ZERO_MV
        self.__we_tot_mv = self.DEFAULT_WE_TOTAL_ZERO_MV

        self.__ae_elc_mv = self.DEFAULT_AE_ELECTRONIC_ZERO_MV
        self.__ae_cal_mv = self.DEFAULT_AE_SENSOR_ZERO_MV
        self.__ae_tot_mv = self.DEFAULT_AE_TOTAL_ZERO_MV

        self.__pcb_gain = self.DEFAULT_PCB_GAIN


    def set_sens_mv_from_sens_na(self):
        we_sens_mv = -0.7313 * self.__we_sens_na + -0.0006          # coefficients found from Alphasense calibrations
        self.__we_sens_mv = round(we_sens_mv, 3)


    def reports_no2_cross_sensitivity(self):
        return self.__we_no2_x_sens_mv is not None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['serial_number'] = self.serial_number
        jdict['sensor_type'] = self.sensor_type

        jdict['we_electronic_zero_mv'] = self.we_elc_mv
        jdict['we_sensor_zero_mv'] = self.we_cal_mv
        jdict['we_total_zero_mv'] = self.we_tot_mv

        jdict['ae_electronic_zero_mv'] = self.ae_elc_mv
        jdict['ae_sensor_zero_mv'] = self.ae_cal_mv
        jdict['ae_total_zero_mv'] = self.ae_tot_mv

        jdict['we_sensitivity_na_ppb'] = self.we_sens_na
        jdict['we_cross_sensitivity_no2_na_ppb'] = self.we_x_sens_na if self.we_x_sens_na else "n/a"

        jdict['pcb_gain'] = self.pcb_gain

        jdict['we_sensitivity_mv_ppb'] = self.we_sens_mv
        jdict['we_cross_sensitivity_no2_mv_ppb'] = self.we_no2_x_sens_mv if self.we_no2_x_sens_mv else "n/a"

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def we_elc_mv(self):
        return self.__we_elc_mv


    @property
    def we_cal_mv(self):
        return self.__we_cal_mv


    @property
    def we_tot_mv(self):
        return self.__we_tot_mv


    @property
    def ae_elc_mv(self):
        return self.__ae_elc_mv


    @property
    def ae_cal_mv(self):
        return self.__ae_cal_mv


    @property
    def ae_tot_mv(self):
        return self.__ae_tot_mv


    @property
    def we_sens_na(self):
        return self.__we_sens_na


    @property
    def we_x_sens_na(self):
        return self.__we_x_sens_na


    @property
    def pcb_gain(self):
        return self.__pcb_gain


    @property
    def we_sens_mv(self):
        return self.__we_sens_mv


    @we_sens_mv.setter
    def we_sens_mv(self, we_sens_mv):
        self.__we_sens_mv = we_sens_mv


    @property
    def we_no2_x_sens_mv(self):
        return self.__we_no2_x_sens_mv


    @we_no2_x_sens_mv.setter
    def we_no2_x_sens_mv(self, we_no2_x_sens_mv):
        self.__we_no2_x_sens_mv = we_no2_x_sens_mv


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "A4Calib:{serial_number:%s, sensor_type:%s, we_elc_mv:%s, we_cal_mv:%s, we_tot_mv:%s, " \
               "ae_elc_mv:%s, ae_cal_mv:%s, ae_tot_mv:%s, we_sens_na:%s, we_x_sens_na:%s, pcb_gain:%s, " \
               "we_sens_mv:%s, we_no2_x_sens_mv:%s}" % \
                    (self.serial_number, self.sensor_type, self.we_elc_mv, self.we_cal_mv, self.we_tot_mv,
                     self.ae_elc_mv, self.ae_cal_mv, self.ae_tot_mv, self.we_sens_na, self.we_x_sens_na, self.pcb_gain,
                     self.we_sens_mv, self.we_no2_x_sens_mv)
