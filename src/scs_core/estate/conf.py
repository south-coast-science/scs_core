"""
Created on 27 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
"""

from collections import OrderedDict

from scs_core.climate.mpl115a2_calib import MPL115A2Calib
from scs_core.climate.mpl115a2_conf import MPL115A2Conf
from scs_core.climate.sht_conf import SHTConf

from scs_core.comms.mqtt_conf import MQTTConf

from scs_core.csv.csv_logger_conf import CSVLoggerConf

from scs_core.data.json import JSONable

from scs_core.display.display_conf import DisplayConf

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.afe.pt1000_calib import Pt1000Calib
from scs_core.gas.ndir.ndir_conf import NDIRConf

from scs_core.gps.gps_conf import GPSConf

from scs_core.interface.interface_conf import InterfaceConf

from scs_core.location.timezone_conf import TimezoneConf

from scs_core.model.gas.gas_baseline import GasBaseline
from scs_core.model.gas.gas_model_conf import GasModelConf
from scs_core.model.pmx.pmx_model_conf import PMxModelConf

from scs_core.particulate.opc_conf import OPCConf

from scs_core.psu.batt_pack.fuel_gauge.max17055.max17055_params import Max17055Params
from scs_core.psu.psu_conf import PSUConf

from scs_core.sync.schedule import Schedule

from scs_core.sys.shared_secret import SharedSecret
from scs_core.sys.system_id import SystemID


# TODO: scd30_conf field
# TODO: run save before doing comparisons to clear datetime millis, etc.

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

        afe_baseline = AFEBaseline.construct_from_jdict(jdict.get('afe-baseline'))
        afe_calib = AFECalib.construct_from_jdict(jdict.get('afe-calib'))
        csv_logger_conf = CSVLoggerConf.construct_from_jdict(jdict.get('csv-logger-conf'))
        display_conf = DisplayConf.construct_from_jdict(jdict.get('display-conf'))
        gas_baseline = GasBaseline.construct_from_jdict(jdict.get('gas-baseline'))
        gas_model_conf = GasModelConf.construct_from_jdict(jdict.get('gas-model-conf'))
        gps_conf = GPSConf.construct_from_jdict(jdict.get('gps-conf'))
        interface_conf = InterfaceConf.construct_from_jdict(jdict.get('interface-conf'))
        max17055_params = Max17055Params.construct_from_jdict(jdict.get('max17055-params'))
        mpl115a2_calib = MPL115A2Calib.construct_from_jdict(jdict.get('mpl115a2-calib'))
        mpl115a2_conf = MPL115A2Conf.construct_from_jdict(jdict.get('mpl115a2-conf'))
        mqtt_conf = MQTTConf.construct_from_jdict(jdict.get('mqtt-conf'))
        ndir_conf = NDIRConf.construct_from_jdict(jdict.get('ndir-conf'))
        opc_conf = OPCConf.construct_from_jdict(jdict.get('opc-conf'))
        pmx_model_conf = PMxModelConf.construct_from_jdict(jdict.get('pmx-model-conf'))
        psu_conf = PSUConf.construct_from_jdict(jdict.get('psu-conf'))
        pt1000_calib = Pt1000Calib.construct_from_jdict(jdict.get('pt1000-calib'))
        schedule = Schedule.construct_from_jdict(jdict.get('schedule'))
        shared_secret = SharedSecret.construct_from_jdict(jdict.get('shared-secret'))
        sht_conf = SHTConf.construct_from_jdict(jdict.get('sht-conf'))
        system_id = SystemID.construct_from_jdict(jdict.get('system-id'))
        timezone_conf = TimezoneConf.construct_from_jdict(jdict.get('timezone-conf'))

        return cls(afe_baseline, afe_calib, csv_logger_conf, display_conf, gas_baseline,
                   gas_model_conf, gps_conf, interface_conf, max17055_params, mpl115a2_calib,
                   mpl115a2_conf, mqtt_conf, ndir_conf, opc_conf, pmx_model_conf, psu_conf,
                   pt1000_calib, schedule, shared_secret, sht_conf, system_id, timezone_conf)


    @classmethod
    def load(cls, manager):
        afe_baseline = AFEBaseline.load(manager)
        afe_calib = AFECalib.load(manager)
        csv_logger_conf = CSVLoggerConf.load(manager)
        display_conf = DisplayConf.load(manager)
        gas_baseline = GasBaseline.load(manager)
        gas_model_conf = GasModelConf.load(manager)
        gps_conf = GPSConf.load(manager)
        interface_conf = InterfaceConf.load(manager)
        max17055_params = Max17055Params.load(manager)
        mpl115a2_calib = MPL115A2Calib.load(manager)
        mpl115a2_conf = MPL115A2Conf.load(manager)
        mqtt_conf = MQTTConf.load(manager)
        ndir_conf = NDIRConf.load(manager)
        opc_conf = OPCConf.load(manager)
        pmx_model_conf = PMxModelConf.load(manager)
        psu_conf = PSUConf.load(manager)
        pt1000_calib = Pt1000Calib.load(manager)
        schedule = Schedule.load(manager)
        shared_secret = SharedSecret.load(manager)
        sht_conf = SHTConf.load(manager)
        system_id = SystemID.load(manager)
        timezone_conf = TimezoneConf.load(manager)

        return cls(afe_baseline, afe_calib, csv_logger_conf, display_conf, gas_baseline,
                   gas_model_conf, gps_conf, interface_conf, max17055_params, mpl115a2_calib,
                   mpl115a2_conf, mqtt_conf, ndir_conf, opc_conf, pmx_model_conf, psu_conf,
                   pt1000_calib, schedule, shared_secret, sht_conf, system_id, timezone_conf)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, afe_baseline, afe_calib, csv_logger_conf, display_conf, gas_baseline,
                 gas_model_conf, gps_conf, interface_conf, max17055_params, mpl115a2_calib,
                 mpl115a2_conf, mqtt_conf, ndir_conf, opc_conf, pmx_model_conf, psu_conf,
                 pt1000_calib, schedule, shared_secret, sht_conf, system_id, timezone_conf):
        """
        Constructor
        """
        self.__afe_baseline = afe_baseline                      # AFEBaseline
        self.__afe_calib = afe_calib                            # AFECalib
        self.__csv_logger_conf = csv_logger_conf                # CSVLoggerConf
        self.__display_conf = display_conf                      # DisplayConf
        self.__gas_baseline = gas_baseline                      # GasBaseline
        self.__gas_model_conf = gas_model_conf                  # GasModelConf
        self.__gps_conf = gps_conf                              # GPSConf
        self.__interface_conf = interface_conf                  # InterfaceConf
        self.__max17055_params = max17055_params                # Max17055Params
        self.__mpl115a2_calib = mpl115a2_calib                  # MPL115A2Calib
        self.__mpl115a2_conf = mpl115a2_conf                    # MPL115A2Conf
        self.__mqtt_conf = mqtt_conf                            # MQTTConf
        self.__ndir_conf = ndir_conf                            # NDIRConf
        self.__opc_conf = opc_conf                              # OPCConf
        self.__pmx_model_conf = pmx_model_conf                  # PMxModelConf
        self.__psu_conf = psu_conf                              # PSUConf
        self.__pt1000_calib = pt1000_calib                      # Pt1000Calib
        self.__schedule = schedule                              # Schedule
        self.__shared_secret = shared_secret                    # SharedSecret
        self.__sht_conf = sht_conf                              # SHTConf
        self.__system_id = system_id                            # SystemID
        self.__timezone_conf = timezone_conf                    # TimezoneConf


    def __eq__(self, other):
        try:
            return self.afe_baseline == other.afe_baseline and self.afe_calib == other.afe_calib and \
                   self.csv_logger_conf == other.csv_logger_conf and self.display_conf == other.display_conf and \
                   self.gas_baseline == other.gas_baseline and self.gas_model_conf == other.gas_model_conf and \
                   self.gps_conf == other.gps_conf and self.interface_conf == other.interface_conf and \
                   self.max17055_params == other.max17055_params and self.mpl115a2_calib == other.mpl115a2_calib and \
                   self.mqtt_conf == other.mqtt_conf and self.ndir_conf == other.ndir_conf and \
                   self.opc_conf == other.opc_conf and self.pmx_model_conf == other.pmx_model_conf and \
                   self.psu_conf == other.psu_conf and self.pt1000_calib == other.pt1000_calib and \
                   self.schedule == other.schedule and self.shared_secret == other.shared_secret and \
                   self.sht_conf == other.sht_conf and self.system_id == other.system_id and \
                   self.timezone_conf == other.timezone_conf

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager):
        pass
        # TODO: implement save(..)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['afe-baseline'] = self.afe_baseline
        jdict['afe-calib'] = self.afe_calib
        jdict['csv-logger-conf'] = self.csv_logger_conf
        jdict['display-conf'] = self.display_conf
        jdict['gas-baseline'] = self.gas_baseline
        jdict['gas-model-conf'] = self.gas_model_conf
        jdict['gps-conf'] = self.gps_conf
        jdict['interface-conf'] = self.interface_conf
        jdict['max17055-params'] = self.max17055_params
        jdict['mpl115a2-calib'] = self.mpl115a2_calib
        jdict['mpl115a2-conf'] = self.mpl115a2_conf
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
    def mpl115a2_conf(self):
        return self.__mpl115a2_conf


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
        return "Conf:{afe_baseline:%s, afe_calib:%s, csv_logger_conf:%s, display_conf:%s, gas_baseline:%s, " \
               "gas_model_conf:%s, gps_conf:%s, interface_conf:%s, max17055_params:%s, mpl115a2_calib:%s, " \
               "mpl115a2_conf:%s, mqtt_conf:%s, ndir_conf:%s, opc_conf:%s, pmx_model_conf:%s, psu_conf:%s, " \
               "pt1000_calib:%s, schedule:%s, shared_secret:%s, sht_conf:%s, system_id:%s, timezone_conf:%s}" % \
               (self.afe_baseline, self.afe_calib, self.csv_logger_conf, self.display_conf, self.gas_baseline,
                self.gas_model_conf, self.gps_conf, self.interface_conf, self.max17055_params, self.mpl115a2_calib,
                self.mpl115a2_conf, self.mqtt_conf, self.ndir_conf, self.opc_conf, self.pmx_model_conf, self.psu_conf,
                self.pt1000_calib, self.schedule, self.shared_secret, self.sht_conf, self.system_id, self.timezone_conf)
