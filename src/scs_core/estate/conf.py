"""
Created on 8 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class Conf(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        afe_baseline = jdict.get('afe-baseline')
        afe_calib = jdict.get('afe-calib')
        csv_logger_conf = jdict.get('csv-logger-conf')
        dfe_conf = jdict.get('dfe-conf')
        display_conf = jdict.get('display-conf')
        gas_baseline = jdict.get('gas-baseline')
        gas_model_conf = jdict.get('gas-model-conf')
        gps_conf = jdict.get('gps-conf')
        interface_conf = jdict.get('interface-conf')
        max17055_params = jdict.get('max17055-params')
        mpl115a2_calib = jdict.get('mpl115a2-calib')
        mqtt_conf = jdict.get('mqtt-conf')
        ndir_conf = jdict.get('ndir-conf')
        opc_conf = jdict.get('opc-conf')
        pmx_model_conf = jdict.get('pmx-model-conf')
        psu_conf = jdict.get('psu-conf')
        pt1000_calib = jdict.get('pt1000-calib')
        schedule = jdict.get('schedule')
        shared_secret = jdict.get('shared-secret')
        sht_conf = jdict.get('sht-conf')
        system_id = jdict.get('system-id')
        timezone_conf = jdict.get('timezone-conf')

        return Conf(afe_baseline, afe_calib, csv_logger_conf, dfe_conf, display_conf,
                    gas_baseline, gas_model_conf, gps_conf, interface_conf, max17055_params,
                    mpl115a2_calib, mqtt_conf, ndir_conf, opc_conf, pmx_model_conf, psu_conf,
                    pt1000_calib, schedule, shared_secret, sht_conf, system_id, timezone_conf)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, afe_baseline, afe_calib, csv_logger_conf, dfe_conf, display_conf,
                 gas_baseline, gas_model_conf, gps_conf, interface_conf, max17055_params,
                 mpl115a2_calib, mqtt_conf, ndir_conf, opc_conf, pmx_model_conf, psu_conf,
                 pt1000_calib, schedule, shared_secret, sht_conf, system_id, timezone_conf):
        """
        Constructor
        """
        self.__afe_baseline = afe_baseline                      # string
        self.__afe_calib = afe_calib                            # string
        self.__csv_logger_conf = csv_logger_conf                # string
        self.__dfe_conf = dfe_conf                              # XX
        self.__display_conf = display_conf                      # XX
        self.__gas_baseline = gas_baseline                      # XX
        self.__gas_model_conf = gas_model_conf                  # XX
        self.__gps_conf = gps_conf                              # XX
        self.__interface_conf = interface_conf                  # XX
        self.__max17055_params = max17055_params                # XX
        self.__mpl115a2_calib = mpl115a2_calib                  # XX
        self.__mqtt_conf = mqtt_conf                            # XX
        self.__ndir_conf = ndir_conf                            # XX
        self.__opc_conf = opc_conf                              # XX
        self.__pmx_model_conf = pmx_model_conf                  # XX
        self.__psu_conf = psu_conf                              # XX
        self.__pt1000_calib = pt1000_calib                      # XX
        self.__schedule = schedule                              # XX
        self.__shared_secret = shared_secret                    # string
        self.__sht_conf = sht_conf                              # XX
        self.__system_id = system_id                            # XX
        self.__timezone_conf = timezone_conf                    # XX


    def __eq__(self, other):
        try:
            return self.afe_baseline == other.afe_baseline and self.afe_calib == other.afe_calib and \
                   self.csv_logger_conf == other.csv_logger_conf and self.dfe_conf == other.dfe_conf and \
                   self.display_conf == other.display_conf and self.gas_baseline == other.gas_baseline and \
                   self.gas_model_conf == other.gas_model_conf and self.gps_conf == other.gps_conf and \
                   self.interface_conf == other.interface_conf and self.max17055_params == other.max17055_params and \
                   self.mpl115a2_calib == other.mpl115a2_calib and self.mqtt_conf == other.mqtt_conf and \
                   self.ndir_conf == other.ndir_conf and self.opc_conf == other.opc_conf and \
                   self.pmx_model_conf == other.pmx_model_conf and self.psu_conf == other.psu_conf and \
                   self.pt1000_calib == other.pt1000_calib and self.schedule == other.schedule and \
                   self.shared_secret == other.shared_secret and self.sht_conf == other.sht_conf and \
                   self.system_id == other.system_id and self.timezone_conf == other.timezone_conf

        except (TypeError, AttributeError):
            return False


        # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['afe-baseline'] = self.afe_baseline
        jdict['afe-calib'] = self.afe_calib
        jdict['csv-logger-conf'] = self.csv_logger_conf
        jdict['dfe-conf'] = self.dfe_conf
        jdict['display-conf'] = self.display_conf
        jdict['gas-baseline'] = self.gas_baseline
        jdict['gas-model-conf'] = self.gas_model_conf
        jdict['gps-conf'] = self.gps_conf
        jdict['interface-conf'] = self.interface_conf
        jdict['max17055-params'] = self.max17055_params
        jdict['mpl115a2-calib'] = self.mpl115a2_calib
        jdict['mqtt-conf'] = self.mqtt_conf
        jdict['ndir-conf'] = self.ndir_conf
        jdict['opc-conf'] = self.opc_conf
        jdict['pmx-model-conf'] = self.pmx_model_conf
        jdict['psu-conf'] = self.psu_conf
        jdict['pt1000-calib'] = self.pt1000_calib
        jdict['schedule'] = self.schedule
        jdict['shared-secret'] = self.shared_secret
        jdict['sht-conf'] = self.sht_conf
        jdict['system-id'] = self.system_id
        jdict['timezone-conf'] = self.timezone_conf

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def afe_baseline(self):
        return self.__afe_baseline


    @property
    def afe_calib(self):
        return self.__afe_calib


    @property
    def csv_logger_conf(self):
        return self.__csv_logger_conf


    @property
    def dfe_conf(self):
        return self.__dfe_conf


    @property
    def display_conf(self):
        return self.__display_conf


    @property
    def gas_baseline(self):
        return self.__gas_baseline


    @property
    def gas_model_conf(self):
        return self.__gas_model_conf


    @property
    def gps_conf(self):
        return self.__gps_conf


    @property
    def interface_conf(self):
        return self.__interface_conf


    @property
    def mpl115a2_calib(self):
        return self.__mpl115a2_calib


    @property
    def max17055_params(self):
        return self.__max17055_params


    @property
    def mqtt_conf(self):
        return self.__mqtt_conf


    @property
    def ndir_conf(self):
        return self.__ndir_conf


    @property
    def opc_conf(self):
        return self.__opc_conf


    @property
    def pmx_model_conf(self):
        return self.__pmx_model_conf


    @property
    def psu_conf(self):
        return self.__psu_conf


    @property
    def pt1000_calib(self):
        return self.__pt1000_calib


    @property
    def schedule(self):
        return self.__schedule


    @property
    def shared_secret(self):
        return self.__shared_secret


    @property
    def sht_conf(self):
        return self.__sht_conf


    @property
    def system_id(self):
        return self.__system_id


    @property
    def timezone_conf(self):
        return self.__timezone_conf


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Conf:{afe_baseline:%s, afe_calib:%s, csv_logger_conf:%s, dfe_conf:%s, display_conf:%s, " \
               "gas_baseline:%s, gas_model_conf:%s, gps_conf:%s, interface_conf:%s, max17055_params:%s, " \
               "mpl115a2_calib:%s, mqtt_conf:%s, ndir_conf:%s, opc_conf:%s, pmx_model_conf:%s, psu_conf:%s, " \
               "pt1000_calib:%s, schedule:%s, shared_secret:%s, sht_conf:%s, system_id:%s, xx:%s}" % \
               (self.afe_baseline, self.afe_calib, self.csv_logger_conf, self.dfe_conf, self.display_conf,
                self.gas_baseline, self.gas_model_conf, self.gps_conf, self.interface_conf, self.max17055_params,
                self.mpl115a2_calib, self.mqtt_conf, self.ndir_conf, self.opc_conf, self.pmx_model_conf, self.psu_conf,
                self.pt1000_calib, self.schedule, self.shared_secret, self.sht_conf, self.system_id, self.timezone_conf)
