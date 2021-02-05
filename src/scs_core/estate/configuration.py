"""
Created on 27 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import socket

from collections import OrderedDict

from scs_core.aws.client.api_auth import APIAuth
from scs_core.aws.client.client_auth import ClientAuth
from scs_core.aws.config.project import Project
from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration
from scs_core.aws.greengrass.aws_identity import AWSIdentity

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
from scs_core.gas.scd30.scd30_conf import SCD30Conf

from scs_core.gps.gps_conf import GPSConf

from scs_core.interface.interface_conf import InterfaceConf

from scs_core.location.timezone_conf import TimezoneConf

from scs_core.model.gas.gas_baseline import GasBaseline
from scs_core.model.gas.gas_model_conf import GasModelConf
from scs_core.model.pmx.pmx_model_conf import PMxModelConf

from scs_core.particulate.opc_conf import OPCConf

from scs_core.psu.psu_conf import PSUConf

from scs_core.sync.schedule import Schedule

from scs_core.sys.shared_secret import SharedSecret
from scs_core.sys.system_id import SystemID


# --------------------------------------------------------------------------------------------------------------------

class Configuration(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jstr(cls, jstr):
        try:
            return cls.construct_from_jdict(json.loads(jstr))
        except json.decoder.JSONDecodeError:
            return None


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        hostname = jdict.get('hostname')

        afe_baseline = AFEBaseline.construct_from_jdict(jdict.get('afe-baseline'), default=None)
        afe_calib = AFECalib.construct_from_jdict(jdict.get('afe-calib'), default=None)
        aws_api_auth = APIAuth.construct_from_jdict(jdict.get('aws-api-auth'), default=None)
        aws_client_auth = ClientAuth.construct_from_jdict(jdict.get('aws-client-auth'), default=None)
        aws_group_config = AWSGroupConfiguration.construct_from_jdict(jdict.get('aws-group-config'), default=None)
        aws_project = Project.construct_from_jdict(jdict.get('aws-project'), default=None)
        csv_logger_conf = CSVLoggerConf.construct_from_jdict(jdict.get('csv-logger-conf'), default=None)
        display_conf = DisplayConf.construct_from_jdict(jdict.get('display-conf'), default=None)
        gas_baseline = GasBaseline.construct_from_jdict(jdict.get('gas-baseline'), default=None)
        gas_model_conf = GasModelConf.construct_from_jdict(jdict.get('gas-model-conf'), default=None)
        gps_conf = GPSConf.construct_from_jdict(jdict.get('gps-conf'), default=None)
        greengrass_identity = AWSIdentity.construct_from_jdict(jdict.get('greengrass-identity'), default=None)
        interface_conf = InterfaceConf.construct_from_jdict(jdict.get('interface-conf'), default=None)
        mpl115a2_calib = MPL115A2Calib.construct_from_jdict(jdict.get('mpl115a2-calib'), default=None)
        mpl115a2_conf = MPL115A2Conf.construct_from_jdict(jdict.get('mpl115a2-conf'), default=None)
        mqtt_conf = MQTTConf.construct_from_jdict(jdict.get('mqtt-conf'), default=None)
        ndir_conf = NDIRConf.construct_from_jdict(jdict.get('ndir-conf'), default=None)
        opc_conf = OPCConf.construct_from_jdict(jdict.get('opc-conf'), default=None)
        pmx_model_conf = PMxModelConf.construct_from_jdict(jdict.get('pmx-model-conf'), default=None)
        psu_conf = PSUConf.construct_from_jdict(jdict.get('psu-conf'), default=None)
        pt1000_calib = Pt1000Calib.construct_from_jdict(jdict.get('pt1000-calib'), default=None)
        scd30_conf = SCD30Conf.construct_from_jdict(jdict.get('scd30-conf'), default=None)
        schedule = Schedule.construct_from_jdict(jdict.get('schedule'), default=None)
        shared_secret = SharedSecret.construct_from_jdict(jdict.get('shared-secret'), default=None)
        sht_conf = SHTConf.construct_from_jdict(jdict.get('sht-conf'), default=None)
        system_id = SystemID.construct_from_jdict(jdict.get('system-id'), default=None)
        timezone_conf = TimezoneConf.construct_from_jdict(jdict.get('timezone-conf'), default=None)

        return cls(hostname, afe_baseline, afe_calib, aws_api_auth, aws_client_auth,
                   aws_group_config, aws_project, csv_logger_conf, display_conf, gas_baseline,
                   gas_model_conf, gps_conf, greengrass_identity, interface_conf, mpl115a2_calib,
                   mpl115a2_conf, mqtt_conf, ndir_conf, opc_conf, pmx_model_conf, psu_conf,
                   pt1000_calib, scd30_conf, schedule, shared_secret, sht_conf, system_id,
                   timezone_conf)


    @classmethod
    def load(cls, manager):
        hostname = socket.gethostname()

        afe_baseline = AFEBaseline.load(manager, default=None)
        afe_calib = AFECalib.load(manager, default=None)
        aws_api_auth = APIAuth.load(manager, default=None)
        aws_client_auth = ClientAuth.load(manager, default=None)
        aws_group_config = AWSGroupConfiguration.load(manager, default=None)
        aws_project = Project.load(manager, default=None)
        csv_logger_conf = CSVLoggerConf.load(manager, default=None)
        display_conf = DisplayConf.load(manager, default=None)
        gas_baseline = GasBaseline.load(manager, default=None)
        gas_model_conf = GasModelConf.load(manager, default=None)
        gps_conf = GPSConf.load(manager, default=None)
        greengrass_identity = AWSIdentity.load(manager, default=None)
        interface_conf = InterfaceConf.load(manager, default=None)
        mpl115a2_calib = MPL115A2Calib.load(manager, default=None)
        mpl115a2_conf = MPL115A2Conf.load(manager, default=None)
        mqtt_conf = MQTTConf.load(manager, default=None)
        ndir_conf = NDIRConf.load(manager, default=None)
        opc_conf = OPCConf.load(manager, default=None)
        pmx_model_conf = PMxModelConf.load(manager, default=None)
        psu_conf = PSUConf.load(manager, default=None)
        pt1000_calib = Pt1000Calib.load(manager, default=None)
        scd30_conf = SCD30Conf.load(manager, default=None)
        schedule = Schedule.load(manager, default=None)
        shared_secret = SharedSecret.load(manager, default=None)
        sht_conf = SHTConf.load(manager, default=None)
        system_id = SystemID.load(manager, default=None)
        timezone_conf = TimezoneConf.load(manager, default=None)

        return cls(hostname, afe_baseline, afe_calib, aws_api_auth, aws_client_auth,
                   aws_group_config, aws_project, csv_logger_conf, display_conf, gas_baseline,
                   gas_model_conf, gps_conf, greengrass_identity, interface_conf, mpl115a2_calib,
                   mpl115a2_conf, mqtt_conf, ndir_conf, opc_conf, pmx_model_conf, psu_conf,
                   pt1000_calib, scd30_conf, schedule, shared_secret, sht_conf, system_id,
                   timezone_conf)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, hostname, afe_baseline, afe_calib, aws_api_auth, aws_client_auth,
                 aws_group_config, aws_project, csv_logger_conf, display_conf, gas_baseline,
                 gas_model_conf, gps_conf, greengrass_identity, interface_conf, mpl115a2_calib,
                 mpl115a2_conf, mqtt_conf, ndir_conf, opc_conf, pmx_model_conf, psu_conf,
                 pt1000_calib, scd30_conf, schedule, shared_secret, sht_conf, system_id,
                 timezone_conf):
        """
        Constructor
        """
        self.__hostname = hostname                                  # string

        self.__afe_baseline = afe_baseline                          # AFEBaseline
        self.__afe_calib = afe_calib                                # AFECalib
        self.__aws_api_auth = aws_api_auth                          # APIAuth
        self.__aws_client_auth = aws_client_auth                    # ClientAuth
        self.__aws_group_config = aws_group_config                  # AWSGroupConfiguration
        self.__aws_project = aws_project                            # Project
        self.__csv_logger_conf = csv_logger_conf                    # CSVLoggerConf
        self.__display_conf = display_conf                          # DisplayConf
        self.__gas_baseline = gas_baseline                          # GasBaseline
        self.__gas_model_conf = gas_model_conf                      # GasModelConf
        self.__gps_conf = gps_conf                                  # GPSConf
        self.__greengrass_identity = greengrass_identity            # AWSIdentity
        self.__interface_conf = interface_conf                      # InterfaceConf
        self.__mpl115a2_calib = mpl115a2_calib                      # MPL115A2Calib
        self.__mpl115a2_conf = mpl115a2_conf                        # MPL115A2Conf
        self.__mqtt_conf = mqtt_conf                                # MQTTConf
        self.__ndir_conf = ndir_conf                                # NDIRConf
        self.__opc_conf = opc_conf                                  # OPCConf
        self.__pmx_model_conf = pmx_model_conf                      # PMxModelConf
        self.__psu_conf = psu_conf                                  # PSUConf
        self.__pt1000_calib = pt1000_calib                          # Pt1000Calib
        self.__scd30_conf = scd30_conf                              # SCD30Conf
        self.__schedule = schedule                                  # Schedule
        self.__shared_secret = shared_secret                        # SharedSecret
        self.__sht_conf = sht_conf                                  # SHTConf
        self.__system_id = system_id                                # SystemID
        self.__timezone_conf = timezone_conf                        # TimezoneConf


    def __eq__(self, other):
        try:
            return self.hostname == other.hostname and \
                   self.afe_baseline == other.afe_baseline and self.afe_calib == other.afe_calib and \
                   self.aws_api_auth == other.aws_api_auth and self.aws_client_auth == other.aws_client_auth and \
                   self.aws_group_config == other.aws_group_config and self.aws_project == other.aws_project and \
                   self.csv_logger_conf == other.csv_logger_conf and self.display_conf == other.display_conf and \
                   self.gas_baseline == other.gas_baseline and self.gas_model_conf == other.gas_model_conf and \
                   self.gps_conf == other.gps_conf and self.greengrass_identity == other.greengrass_identity and \
                   self.interface_conf == other.interface_conf and self.mpl115a2_calib == other.mpl115a2_calib and \
                   self.mpl115a2_conf == other.mpl115a2_conf and self.mqtt_conf == other.mqtt_conf and \
                   self.ndir_conf == other.ndir_conf and self.opc_conf == other.opc_conf and \
                   self.pmx_model_conf == other.pmx_model_conf and self.psu_conf == other.psu_conf and \
                   self.pt1000_calib == other.pt1000_calib and self.scd30_conf == other.scd30_conf and \
                   self.schedule == other.schedule and self.shared_secret == other.shared_secret and \
                   self.sht_conf == other.sht_conf and self.system_id == other.system_id and \
                   self.timezone_conf == other.timezone_conf

        except (TypeError, AttributeError):
            return False


    def diff(self, other):
        diff = Configuration(None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None, None,
                             None, None, None, None, None, None,
                             None)

        if self.hostname != other.hostname:
            diff.__hostname = self.hostname

        if self.afe_calib != other.afe_calib:
            diff.__afe_calib = self.afe_calib

        if self.aws_api_auth != other.aws_api_auth:
            diff.__aws_api_auth = self.aws_api_auth

        if self.aws_client_auth != other.aws_client_auth:
            diff.__aws_client_auth = self.aws_client_auth

        if self.aws_group_config != other.aws_group_config:
            diff.__aws_group_config = self.aws_group_config

        if self.aws_project != other.aws_project:
            diff.__aws_project = self.aws_project

        if self.csv_logger_conf != other.csv_logger_conf:
            diff.__csv_logger_conf = self.csv_logger_conf

        if self.display_conf != other.display_conf:
            diff.__display_conf = self.display_conf

        if self.gas_baseline != other.gas_baseline:
            diff.__gas_baseline = self.gas_baseline

        if self.gas_model_conf != other.gas_model_conf:
            diff.__gas_model_conf = self.gas_model_conf

        if self.gps_conf != other.gps_conf:
            diff.__gps_conf = self.gps_conf

        if self.greengrass_identity != other.greengrass_identity:
            diff.__greengrass_identity = self.greengrass_identity

        if self.interface_conf != other.interface_conf:
            diff.__interface_conf = self.interface_conf

        if self.mpl115a2_calib != other.mpl115a2_calib:
            diff.__mpl115a2_calib = self.mpl115a2_calib

        if self.mpl115a2_conf != other.mpl115a2_conf:
            diff.__mpl115a2_conf = self.mpl115a2_conf

        if self.mqtt_conf != other.mqtt_conf:
            diff.__mqtt_conf = self.mqtt_conf

        if self.ndir_conf != other.ndir_conf:
            diff.__ndir_conf = self.ndir_conf

        if self.opc_conf != other.opc_conf:
            diff.__opc_conf = self.opc_conf

        if self.pmx_model_conf != other.pmx_model_conf:
            diff.__pmx_model_conf = self.pmx_model_conf

        if self.psu_conf != other.psu_conf:
            diff.__psu_conf = self.psu_conf

        if self.pt1000_calib != other.pt1000_calib:
            diff.__pt1000_calib = self.pt1000_calib

        if self.scd30_conf != other.scd30_conf:
            diff.__scd30_conf = self.scd30_conf

        if self.schedule != other.schedule:
            diff.__schedule = self.schedule

        if self.shared_secret != other.shared_secret:
            diff.__shared_secret = self.shared_secret

        if self.sht_conf != other.sht_conf:
            diff.__sht_conf = self.sht_conf

        if self.system_id != other.system_id:
            diff.__system_id = self.system_id

        if self.timezone_conf != other.timezone_conf:
            diff.__timezone_conf = self.timezone_conf

        return diff


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager):
        if self.afe_baseline:
            self.afe_baseline.save(manager)

        if self.afe_calib:
            self.afe_calib.save(manager)

        if self.aws_api_auth:
            self.aws_api_auth.save(manager)

        if self.aws_client_auth:
            self.aws_client_auth.save(manager)

        if self.aws_group_config:
            self.aws_group_config.save(manager)

        if self.aws_project:
            self.aws_project.save(manager)

        if self.csv_logger_conf:
            self.csv_logger_conf.save(manager)

        if self.display_conf:
            self.display_conf.save(manager)

        if self.gas_baseline:
            self.gas_baseline.save(manager)

        if self.gas_model_conf:
            self.gas_model_conf.save(manager)

        if self.gps_conf:
            self.gps_conf.save(manager)

        if self.greengrass_identity:
            self.greengrass_identity.save(manager)

        if self.interface_conf:
            self.interface_conf.save(manager)

        if self.mpl115a2_calib:
            self.mpl115a2_calib.save(manager)

        if self.mpl115a2_conf:
            self.mpl115a2_conf.save(manager)

        if self.mqtt_conf:
            self.mqtt_conf.save(manager)

        if self.ndir_conf:
            self.ndir_conf.save(manager)

        if self.opc_conf:
            self.opc_conf.save(manager)

        if self.pmx_model_conf:
            self.pmx_model_conf.save(manager)

        if self.psu_conf:
            self.psu_conf.save(manager)

        if self.pt1000_calib:
            self.pt1000_calib.save(manager)

        if self.scd30_conf:
            self.scd30_conf.save(manager)

        if self.schedule:
            self.schedule.save(manager)

        if self.shared_secret:
            self.shared_secret.save(manager)

        if self.sht_conf:
            self.sht_conf.save(manager)

        if self.system_id:
            self.system_id.save(manager)

        if self.timezone_conf:
            self.timezone_conf.save(manager)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['hostname'] = self.hostname

        jdict['afe-baseline'] = self.afe_baseline
        jdict['afe-calib'] = self.afe_calib
        jdict['aws-api-auth'] = self.aws_api_auth
        jdict['aws-client-auth'] = self.aws_client_auth
        jdict['aws-group-config'] = self.aws_group_config
        jdict['aws-project'] = self.aws_project
        jdict['csv-logger-conf'] = self.csv_logger_conf
        jdict['display-conf'] = self.display_conf
        jdict['gas-baseline'] = self.gas_baseline
        jdict['gas-model-conf'] = self.gas_model_conf
        jdict['gps-conf'] = self.gps_conf
        jdict['interface-conf'] = self.interface_conf
        jdict['greengrass-identity'] = self.greengrass_identity
        jdict['mpl115a2-calib'] = self.mpl115a2_calib
        jdict['mpl115a2-conf'] = self.mpl115a2_conf
        jdict['mqtt-conf'] = self.mqtt_conf
        jdict['ndir-conf'] = self.ndir_conf
        jdict['opc-conf'] = self.opc_conf
        jdict['pmx-model-conf'] = self.pmx_model_conf
        jdict['psu-conf'] = self.psu_conf
        jdict['pt1000-calib'] = self.pt1000_calib
        jdict['scd30-conf'] = self.scd30_conf
        jdict['schedule'] = self.schedule
        jdict['shared-secret'] = self.shared_secret
        jdict['sht-conf'] = self.sht_conf
        jdict['system-id'] = self.system_id
        jdict['timezone-conf'] = self.timezone_conf

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def hostname(self):
        return self.__hostname


    @property
    def afe_baseline(self):
        return self.__afe_baseline


    @property
    def afe_calib(self):
        return self.__afe_calib


    @property
    def aws_api_auth(self):
        return self.__aws_api_auth


    @property
    def aws_client_auth(self):
        return self.__aws_client_auth


    @property
    def aws_group_config(self):
        return self.__aws_group_config


    @property
    def aws_project(self):
        return self.__aws_project


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
    def greengrass_identity(self):
        return self.__greengrass_identity


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
    def scd30_conf(self):
        return self.__scd30_conf


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
        return "Configuration:{hostname:%s, afe_baseline:%s, afe_calib:%s, aws_api_auth:%s, aws_client_auth:%s, " \
               "aws_group_config:%s, aws_project:%s, csv_logger_conf:%s, display_conf:%s, gas_baseline:%s, " \
               "gas_model_conf:%s, gps_conf:%s, greengrass_identity:%s, interface_conf:%s, mpl115a2_calib:%s, " \
               "mpl115a2_conf:%s, mqtt_conf:%s, ndir_conf:%s, opc_conf:%s, pmx_model_conf:%s, psu_conf:%s, " \
               "pt1000_calib:%s, scd30_conf:%s, schedule:%s, shared_secret:%s, sht_conf:%s, system_id:%s, " \
               "timezone_conf:%s}" % \
               (self.hostname, self.afe_baseline, self.afe_calib, self.aws_api_auth, self.aws_client_auth,
                self.aws_group_config, self.aws_project, self.csv_logger_conf, self.display_conf, self.gas_baseline,
                self.gas_model_conf, self.gps_conf, self.greengrass_identity, self.interface_conf, self.mpl115a2_calib,
                self.mpl115a2_conf, self.mqtt_conf, self.ndir_conf, self.opc_conf, self.pmx_model_conf, self.psu_conf,
                self.pt1000_calib, self.scd30_conf, self.schedule, self.shared_secret, self.sht_conf, self.system_id,
                self.timezone_conf)
