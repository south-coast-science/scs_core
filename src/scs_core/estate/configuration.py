"""
Created on 27 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{
    "rec": "2021-11-02T10:53:15Z",
    "tag": "scs-opc-1",
    "ver": 1.0,
    "val": {
        "hostname": "scs-cube-001",
        "packs": {
            "scs_core": {
                "repo": "scs_core",
                "version": "1.1.1"
            },
            "scs_dev": {
                "repo": "scs_dev",
                "version": "1.1.1"
            },
            "scs_dfe": {
                "repo": "scs_dfe_eng",
                "version": "1.1.0"
            },
            "scs_greengrass": {
                "repo": "scs_greengrass",
                "version": "2.1.2"
            },
            "scs_host": {
                "repo": "scs_host_cpc",
                "version": "1.0.5"
            },
            "scs_inference": {
                "repo": "scs_inference",
                "version": null
            },
            "scs_mfr": {
                "repo": "scs_mfr",
                "version": "1.1.1"
            },
            "scs_ndir": {
                "repo": "scs_ndir",
                "version": null
            },
            "scs_psu": {
                "repo": "scs_psu",
                "version": "1.0.10"
            }
        },
        "afe-baseline": {
            "sn1": {
                "calibrated-on": "2021-11-01T17:43:41Z",
                "offset": 120
            },
            "sn2": {
                "calibrated-on": "2021-11-01T17:32:48Z",
                "offset": 0
            },
            "sn3": {
                "calibrated-on": "2021-11-01T17:32:48Z",
                "offset": 0
            },
            "sn4": {
                "calibrated-on": "2021-11-01T17:32:48Z",
                "offset": 0
            }
        },
        "afe-id": {
            "serial_number": null,
            "type": "DSI",
            "calibrated_on": "2020-01-01",
            "sn1": {
                "serial_number": "212060325",
                "sensor_type": "NOGA4"
            }
        },
        "aws-api-auth": {
            "endpoint": "aws.southcoastscience.com",
            "api-key": "de92c5ff-b47a-4cc4-a04c-62d684d64a1f"
        },
        "aws-group-config": {
            "group-name": "scs-cube-001-group",
            "time-initiated": "2021-02-08T16:38:55Z",
            "unix-group": 984,
            "ml": true
        },
        "aws-project": {
            "location-path": "south-coast-science-dev/cube/loc/1",
            "device-path": "south-coast-science-dev/cube/device"
        },
        "csv-logger-conf": {
            "root-path": "/srv/removable_data_storage",
            "delete-oldest": true,
            "write-interval": 0
        },
        "display-conf": null,
        "vcal-baseline": {
            "NO2": {
                "calibrated-on": "2021-11-01T17:33:10Z",
                "offset": 107
            }
        },
        "gas-baseline": {
            "NO2": {
                "calibrated-on": "2021-11-01T09:30:50Z",
                "offset": 0
            }
        },
        "gas-model-conf": {
            "uds-path": "pipes/lambda-gas-model.uds",
            "model-interface": "vE",
            "model-compendium-group": "OE21HA"
        },
        "gps-conf": {
            "model": "SAM8Q",
            "sample-interval": 10,
            "tally": 60,
            "report-file": "/tmp/southcoastscience/gps_report.json",
            "debug": false
        },
        "interface-conf": {
            "model": "OPCubeT1"
        },
        "greengrass-identity": {
            "core-name": "scs-cube-001-core",
            "group-name": "scs-cube-001-group"
        },
        "mpl115a2-calib": null,
        "mqtt-conf": {
            "inhibit-publishing": false,
            "report-file": "/tmp/southcoastscience/mqtt_queue_report.json",
            "debug": false
        },
        "ndir-conf": null,
        "opc-conf": {
            "model": "N3",
            "sample-period": 10,
            "restart-on-zeroes": true,
            "power-saving": false
        },
        "opc-version": {
            "serial": "177336702",
            "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"
        },
        "pmx-model-conf": {
            "uds-path": "pipes/lambda-pmx-model.uds",
            "model-interface": "s2"
        },
        "pressure-conf": null,
        "psu-conf": {
            "model": "OPCubeV1",
            "batt-model": "PackV2",
            "ignore-threshold": true,
            "reporting-interval": 5,
            "report-file": "/tmp/southcoastscience/psu_status_report.json"
        },
        "psu-version": {
            "id": "SCS OPCube Controller type 1 firmware 1",
            "tag": "001.001.003",
            "c-date": null,
            "c-time": null
        },
        "pt1000-calib": null,
        "scd30-baseline": null,
        "scd30-conf": null,
        "schedule": {
            "scs-climate": {
                "interval": 60.0,
                "tally": 1
            },
            "scs-gases": {
                "interval": 10.0,
                "tally": 1
            },
            "scs-particulates": {
                "interval": 10.0,
                "tally": 1
            },
            "scs-status": {
                "interval": 60.0,
                "tally": 1
            }
        },
        "shared-secret": {
            "key": "Ytzglk6oYpzJY0FB"
        },
        "sht-conf": {
            "int": "0x45",
            "ext": "0x45"
        },
        "networks": {
            "eth0": {
                "kind": "ethernet",
                "state": "connected",
                "connection": "Ethernet eth0"
            },
            "cdc-wdm0": {
                "kind": "gsm",
                "state": "connecting",
                "connection": "(prepare)  Claro_Brazil"
            }
        },
        "modem": {
            "id": "3f07553c31ce11715037ac16c24ceddcfb6f7a0b",
            "imei": "867962041294151",
            "mfr": "QUALCOMM INCORPORATED",
            "model": "QUECTEL Mobile Broadband Module",
            "rev": "EC21EFAR06A01M4G"
        },
        "sim": {
            "imsi": "234104886708667",
            "iccid": "8944110068256270054",
            "operator-code": null,
            "operator-name": null
        },
        "system-id": {
            "set-on": "2020-09-17T11:16:25Z",
            "vendor-id": "SCS",
            "model-id": "OPC",
            "model": "Praxis/OPCube",
            "config": "v1",
            "system-sn": 1
        },
        "timezone-conf": {
            "set-on": "2017-08-15T12:50:05Z",
            "name": "Europe/London"
        }
    }
}
"""

import json
import socket

from collections import OrderedDict

from scs_core.aws.client.api_auth import APIAuth
from scs_core.aws.config.project import Project
from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration
from scs_core.aws.greengrass.aws_identity import AWSIdentity

from scs_core.climate.mpl115a2_calib import MPL115A2Calib
from scs_core.climate.pressure_conf import PressureConf
from scs_core.climate.sht_conf import SHTConf

from scs_core.comms.mqtt_conf import MQTTConf

from scs_core.csv.csv_logger_conf import CSVLoggerConf

from scs_core.data.json import JSONable

from scs_core.display.display_conf import DisplayConf

from scs_core.estate.package_version import PackageVersions

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_id import AFEId
from scs_core.gas.afe.pt1000_calib import Pt1000Calib
from scs_core.gas.ndir.ndir_conf import NDIRConf
from scs_core.gas.scd30.scd30_conf import SCD30Conf
from scs_core.gas.scd30.scd30_baseline import SCD30Baseline

from scs_core.gps.gps_conf import GPSConf

from scs_core.interface.interface_conf import InterfaceConf

from scs_core.location.timezone_conf import TimezoneConf

from scs_core.model.gas.gas_baseline import GasBaseline
from scs_core.model.gas.gas_model_conf import GasModelConf
from scs_core.model.gas.vcal_baseline import VCalBaseline

from scs_core.model.pmx.pmx_model_conf import PMxModelConf

from scs_core.particulate.opc_conf import OPCConf
from scs_core.particulate.opc_version import OPCVersion

from scs_core.psu.psu_conf import PSUConf
from scs_core.psu.psu_version import PSUVersion

from scs_core.sync.schedule import Schedule

from scs_core.sys.modem import Modem, SIM
from scs_core.sys.network import Networks
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
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            if skeleton:
                return cls(None, None, None, None, None,
                           None, None, None, None, None,
                           None, None, None, None, None,
                           None, None, None, None, None,
                           None, None, None, None, None,
                           None, None, None, None, None,
                           None, None, None, None, None)
            else:
                return None

        hostname = jdict.get('hostname')
        packs = PackageVersions.construct_from_jdict(jdict.get('packs'))

        afe_baseline = AFEBaseline.construct_from_jdict(jdict.get('afe-baseline'))
        afe_id = AFEId.construct_from_jdict(jdict.get('afe-id'))
        aws_api_auth = APIAuth.construct_from_jdict(jdict.get('aws-api-auth'))
        aws_group_config = AWSGroupConfiguration.construct_from_jdict(jdict.get('aws-group-config'))
        aws_project = Project.construct_from_jdict(jdict.get('aws-project'))
        csv_logger_conf = CSVLoggerConf.construct_from_jdict(jdict.get('csv-logger-conf'))
        display_conf = DisplayConf.construct_from_jdict(jdict.get('display-conf'))
        vcal_baseline = VCalBaseline.construct_from_jdict(jdict.get('vcal-baseline'))
        gas_baseline = GasBaseline.construct_from_jdict(jdict.get('gas-baseline'))
        gas_model_conf = GasModelConf.construct_from_jdict(jdict.get('gas-model-conf'))
        gps_conf = GPSConf.construct_from_jdict(jdict.get('gps-conf'))
        greengrass_identity = AWSIdentity.construct_from_jdict(jdict.get('greengrass-identity'))
        interface_conf = InterfaceConf.construct_from_jdict(jdict.get('interface-conf'))
        mpl115a2_calib = MPL115A2Calib.construct_from_jdict(jdict.get('mpl115a2-calib'))
        mqtt_conf = MQTTConf.construct_from_jdict(jdict.get('mqtt-conf'))
        ndir_conf = NDIRConf.construct_from_jdict(jdict.get('ndir-conf'))
        opc_conf = OPCConf.construct_from_jdict(jdict.get('opc-conf'))
        opc_version = OPCVersion.construct_from_jdict(jdict.get('opc-version'))
        pmx_model_conf = PMxModelConf.construct_from_jdict(jdict.get('pmx-model-conf'))
        pressure_conf = PressureConf.construct_from_jdict(jdict.get('pressure-conf'))
        psu_conf = PSUConf.construct_from_jdict(jdict.get('psu-conf'))
        psu_version = PSUVersion.construct_from_jdict(jdict.get('psu-version'))
        pt1000_calib = Pt1000Calib.construct_from_jdict(jdict.get('pt1000-calib'))
        scd30_baseline = SCD30Baseline.construct_from_jdict(jdict.get('scd30-baseline'))
        scd30_conf = SCD30Conf.construct_from_jdict(jdict.get('scd30-conf'))
        schedule = Schedule.construct_from_jdict(jdict.get('schedule'))
        shared_secret = SharedSecret.construct_from_jdict(jdict.get('shared-secret'))
        sht_conf = SHTConf.construct_from_jdict(jdict.get('sht-conf'))
        networks = Networks.construct_from_jdict(jdict.get('networks'))
        modem = Modem.construct_from_jdict(jdict.get('modem'))
        sim = SIM.construct_from_jdict(jdict.get('sim'))
        system_id = SystemID.construct_from_jdict(jdict.get('system-id'))
        timezone_conf = TimezoneConf.construct_from_jdict(jdict.get('timezone-conf'))

        return cls(hostname, packs, afe_baseline, afe_id, aws_api_auth,
                   aws_group_config, aws_project, csv_logger_conf, display_conf,
                   vcal_baseline, gas_baseline, gas_model_conf, gps_conf, greengrass_identity,
                   interface_conf, mpl115a2_calib, mqtt_conf, ndir_conf, opc_conf, opc_version,
                   pmx_model_conf, pressure_conf, psu_conf, psu_version, pt1000_calib,
                   scd30_baseline, scd30_conf, schedule, shared_secret, sht_conf, networks,
                   modem, sim, system_id, timezone_conf)


    @classmethod
    def load(cls, manager, psu_version=None):
        hostname = socket.gethostname()
        packs = PackageVersions.construct_from_installation(manager.scs_path(), manager)

        afe_baseline = AFEBaseline.load(manager)
        afe_id = AFEId.load(manager)
        aws_api_auth = APIAuth.load(manager)
        aws_group_config = AWSGroupConfiguration.load(manager)
        aws_project = Project.load(manager)
        csv_logger_conf = CSVLoggerConf.load(manager)
        display_conf = DisplayConf.load(manager)
        vcal_baseline = VCalBaseline.load(manager)
        gas_baseline = GasBaseline.load(manager)
        gas_model_conf = GasModelConf.load(manager)
        gps_conf = GPSConf.load(manager)
        greengrass_identity = AWSIdentity.load(manager)
        interface_conf = InterfaceConf.load(manager)
        mpl115a2_calib = MPL115A2Calib.load(manager)
        mqtt_conf = MQTTConf.load(manager)
        ndir_conf = NDIRConf.load(manager)
        opc_conf = OPCConf.load(manager)
        opc_version = OPCVersion.load(manager)
        pmx_model_conf = PMxModelConf.load(manager)
        pressure_conf = PressureConf.load(manager)
        psu_conf = PSUConf.load(manager)
        psu_version = psu_version
        pt1000_calib = Pt1000Calib.load(manager)
        scd30_baseline = SCD30Baseline.load(manager)
        scd30_conf = SCD30Conf.load(manager)
        schedule = Schedule.load(manager)
        shared_secret = SharedSecret.load(manager)
        sht_conf = SHTConf.load(manager)
        networks = manager.networks()
        modem = manager.modem()
        sim = manager.sim()
        system_id = SystemID.load(manager)
        timezone_conf = TimezoneConf.load(manager)

        return cls(hostname, packs, afe_baseline, afe_id, aws_api_auth,
                   aws_group_config, aws_project, csv_logger_conf, display_conf,
                   vcal_baseline, gas_baseline, gas_model_conf, gps_conf, greengrass_identity,
                   interface_conf, mpl115a2_calib, mqtt_conf, ndir_conf, opc_conf, opc_version,
                   pmx_model_conf, pressure_conf, psu_conf, psu_version, pt1000_calib,
                   scd30_baseline, scd30_conf, schedule, shared_secret, sht_conf, networks,
                   modem, sim, system_id, timezone_conf)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, hostname, packs, afe_baseline, afe_id, aws_api_auth,
                 aws_group_config, aws_project, csv_logger_conf, display_conf,
                 vcal_baseline, gas_baseline, gas_model_conf, gps_conf, greengrass_identity,
                 interface_conf, mpl115a2_calib, mqtt_conf, ndir_conf, opc_conf, opc_version,
                 pmx_model_conf, pressure_conf, psu_conf, psu_version, pt1000_calib,
                 scd30_baseline, scd30_conf, schedule, shared_secret, sht_conf, networks,
                 modem, sim, system_id, timezone_conf):
        """
        Constructor
        """

        self.__hostname = hostname                                  # string
        self.__packs = packs                                        # PackageVersions

        self.__afe_baseline = afe_baseline                          # AFEBaseline
        self.__afe_id = afe_id                                      # AFEId
        self.__aws_api_auth = aws_api_auth                          # APIAuth
        self.__aws_group_config = aws_group_config                  # AWSGroupConfiguration
        self.__aws_project = aws_project                            # Project
        self.__csv_logger_conf = csv_logger_conf                    # CSVLoggerConf
        self.__display_conf = display_conf                          # DisplayConf
        self.__vcal_baseline = vcal_baseline                        # VCalBaseline
        self.__gas_baseline = gas_baseline                          # GasBaseline
        self.__gas_model_conf = gas_model_conf                      # GasModelConf
        self.__gps_conf = gps_conf                                  # GPSConf
        self.__greengrass_identity = greengrass_identity            # AWSIdentity
        self.__interface_conf = interface_conf                      # InterfaceConf
        self.__mpl115a2_calib = mpl115a2_calib                      # MPL115A2Calib
        self.__mqtt_conf = mqtt_conf                                # MQTTConf
        self.__ndir_conf = ndir_conf                                # NDIRConf
        self.__opc_conf = opc_conf                                  # OPCConf
        self.__opc_version = opc_version                            # OPCVersion
        self.__pmx_model_conf = pmx_model_conf                      # PMxModelConf
        self.__pressure_conf = pressure_conf                        # PressureConf
        self.__psu_conf = psu_conf                                  # PSUConf
        self.__psu_version = psu_version                            # PSUVersion
        self.__pt1000_calib = pt1000_calib                          # Pt1000Calib
        self.__scd30_baseline = scd30_baseline                      # SCD30Baseline
        self.__scd30_conf = scd30_conf                              # SCD30Conf
        self.__schedule = schedule                                  # Schedule
        self.__shared_secret = shared_secret                        # SharedSecret
        self.__sht_conf = sht_conf                                  # SHTConf
        self.__networks = networks                                  # Networks
        self.__modem = modem                                        # Modem
        self.__sim = sim                                            # SIM
        self.__system_id = system_id                                # SystemID
        self.__timezone_conf = timezone_conf                        # TimezoneConf


    def __eq__(self, other):
        try:
            return self.hostname == other.hostname and self.packs == other.packs and \
                   self.afe_baseline == other.afe_baseline and self.afe_id == other.afe_id and \
                   self.aws_api_auth == other.aws_api_auth and self.aws_group_config == other.aws_group_config and \
                   self.aws_project == other.aws_project and self.csv_logger_conf == other.csv_logger_conf and \
                   self.display_conf == other.display_conf and self.vcal_baseline == other.vcal_baseline and \
                   self.gas_baseline == other.gas_baseline and self.gas_model_conf == other.gas_model_conf and \
                   self.gps_conf == other.gps_conf and self.greengrass_identity == other.greengrass_identity and \
                   self.interface_conf == other.interface_conf and self.mpl115a2_calib == other.mpl115a2_calib and \
                   self.mqtt_conf == other.mqtt_conf and self.ndir_conf == other.ndir_conf and \
                   self.opc_conf == other.opc_conf and self.pmx_model_conf == other.pmx_model_conf and \
                   self.pmx_model_conf == other.pmx_model_conf and self.pressure_conf == other.pressure_conf and \
                   self.psu_conf == other.psu_conf and self.psu_version == other.psu_version and \
                   self.pt1000_calib == other.pt1000_calib and self.scd30_baseline == other.scd30_baseline and \
                   self.scd30_conf == other.scd30_conf and self.schedule == other.schedule and \
                   self.shared_secret == other.shared_secret and self.sht_conf == other.sht_conf and \
                   self.networks == other.networks and self.modem == other.modem and \
                   self.sim == other.sim and self.system_id == other.system_id and \
                   self.timezone_conf == other.timezone_conf

        except (TypeError, AttributeError):
            return False


    def diff(self, other):
        diff = Configuration(None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None)

        if self.hostname != other.hostname:
            diff.__hostname = self.hostname

        if self.packs != other.packs:
            diff.__packs = self.packs

        if self.afe_id != other.afe_id:
            diff.__afe_id = self.afe_id

        if self.aws_api_auth != other.aws_api_auth:
            diff.__aws_api_auth = self.aws_api_auth

        if self.aws_group_config != other.aws_group_config:
            diff.__aws_group_config = self.aws_group_config

        if self.aws_project != other.aws_project:
            diff.__aws_project = self.aws_project

        if self.csv_logger_conf != other.csv_logger_conf:
            diff.__csv_logger_conf = self.csv_logger_conf

        if self.display_conf != other.display_conf:
            diff.__display_conf = self.display_conf

        if self.vcal_baseline != other.vcal_baseline:
            diff.__vcal_baseline = self.vcal_baseline

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

        if self.mqtt_conf != other.mqtt_conf:
            diff.__mqtt_conf = self.mqtt_conf

        if self.ndir_conf != other.ndir_conf:
            diff.__ndir_conf = self.ndir_conf

        if self.opc_conf != other.opc_conf:
            diff.__opc_conf = self.opc_conf

        if self.opc_version != other.opc_version:
            diff.__opc_version = self.opc_version

        if self.pmx_model_conf != other.pmx_model_conf:
            diff.__pmx_model_conf = self.pmx_model_conf

        if self.pressure_conf != other.pressure_conf:
            diff.__pressure_conf = self.pressure_conf

        if self.psu_conf != other.psu_conf:
            diff.__psu_conf = self.psu_conf

        if self.psu_version != other.psu_version:
            diff.__psu_version = self.psu_version

        if self.pt1000_calib != other.pt1000_calib:
            diff.__pt1000_calib = self.pt1000_calib

        if self.scd30_baseline != other.scd30_baseline:
            diff.__scd30_baseline = self.scd30_baseline

        if self.scd30_conf != other.scd30_conf:
            diff.__scd30_conf = self.scd30_conf

        if self.schedule != other.schedule:
            diff.__schedule = self.schedule

        if self.shared_secret != other.shared_secret:
            diff.__shared_secret = self.shared_secret

        if self.sht_conf != other.sht_conf:
            diff.__sht_conf = self.sht_conf

        if self.networks != other.networks:
            diff.__networks = self.networks

        if self.modem != other.modem:
            diff.__modem = self.modem

        if self.sim != other.sim:
            diff.__sim = self.sim

        if self.system_id != other.system_id:
            diff.__system_id = self.system_id

        if self.timezone_conf != other.timezone_conf:
            diff.__timezone_conf = self.timezone_conf

        return diff


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager):
        if self.hostname:
            raise ValueError('hostname may not be set')

        if self.packs:
            raise ValueError('packs may not be set')

        if self.afe_baseline:
            self.afe_baseline.save(manager)

        if self.afe_id:
            raise ValueError('afe_id may not be set')

        if self.aws_api_auth:
            self.aws_api_auth.save(manager)

        if self.aws_group_config:
            self.aws_group_config.save(manager)

        if self.aws_project:
            self.aws_project.save(manager)

        if self.csv_logger_conf:
            self.csv_logger_conf.save(manager)

        if self.display_conf:
            self.display_conf.save(manager)

        if self.vcal_baseline:
            self.vcal_baseline.save(manager)

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

        if self.mqtt_conf:
            self.mqtt_conf.save(manager)

        if self.ndir_conf:
            self.ndir_conf.save(manager)

        if self.opc_conf:
            self.opc_conf.save(manager)

        if self.opc_version:
            raise ValueError('opc_version may not be set')

        if self.pmx_model_conf:
            self.pmx_model_conf.save(manager)

        if self.pressure_conf:
            self.pressure_conf.save(manager)

        if self.psu_conf:
            self.psu_conf.save(manager)

        if self.psu_version:
            raise ValueError('psu_version may not be set')

        if self.pt1000_calib:
            self.pt1000_calib.save(manager)

        if self.scd30_baseline:
            self.scd30_baseline.save(manager)

        if self.scd30_conf:
            self.scd30_conf.save(manager)

        if self.schedule:
            self.schedule.save(manager)

        if self.shared_secret:
            self.shared_secret.save(manager)

        if self.sht_conf:
            self.sht_conf.save(manager)

        if self.networks:
            raise ValueError('networks may not be set')

        if self.modem:
            raise ValueError('modem may not be set')

        if self.sim:
            raise ValueError('sim may not be set')

        if self.system_id:
            self.system_id.save(manager)

        if self.timezone_conf:
            self.timezone_conf.save(manager)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['hostname'] = self.hostname
        jdict['packs'] = self.packs

        jdict['afe-baseline'] = self.afe_baseline
        jdict['afe-id'] = self.afe_id
        jdict['aws-api-auth'] = self.aws_api_auth
        jdict['aws-group-config'] = self.aws_group_config
        jdict['aws-project'] = self.aws_project
        jdict['csv-logger-conf'] = self.csv_logger_conf
        jdict['display-conf'] = self.display_conf
        jdict['vcal-baseline'] = self.vcal_baseline
        jdict['gas-baseline'] = self.gas_baseline
        jdict['gas-model-conf'] = self.gas_model_conf
        jdict['gps-conf'] = self.gps_conf
        jdict['interface-conf'] = self.interface_conf
        jdict['greengrass-identity'] = self.greengrass_identity
        jdict['mpl115a2-calib'] = self.mpl115a2_calib
        jdict['mqtt-conf'] = self.mqtt_conf
        jdict['ndir-conf'] = self.ndir_conf
        jdict['opc-conf'] = self.opc_conf
        jdict['opc-version'] = self.opc_version
        jdict['pmx-model-conf'] = self.pmx_model_conf
        jdict['pressure-conf'] = self.pressure_conf
        jdict['psu-conf'] = self.psu_conf
        jdict['psu-version'] = self.psu_version
        jdict['pt1000-calib'] = self.pt1000_calib
        jdict['scd30-baseline'] = self.scd30_baseline
        jdict['scd30-conf'] = self.scd30_conf
        jdict['schedule'] = self.schedule
        jdict['shared-secret'] = self.shared_secret
        jdict['sht-conf'] = self.sht_conf
        jdict['sht-conf'] = self.sht_conf
        jdict['networks'] = self.networks
        jdict['modem'] = self.modem
        jdict['sim'] = self.sim
        jdict['system-id'] = self.system_id
        jdict['timezone-conf'] = self.timezone_conf

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def hostname(self):
        return self.__hostname


    @property
    def packs(self):
        return self.__packs


    @property
    def afe_baseline(self):
        return self.__afe_baseline


    @property
    def afe_id(self):
        return self.__afe_id


    @property
    def aws_api_auth(self):
        return self.__aws_api_auth


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
    def vcal_baseline(self):
        return self.__vcal_baseline


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
    def mqtt_conf(self):
        return self.__mqtt_conf


    @property
    def ndir_conf(self):
        return self.__ndir_conf


    @property
    def opc_conf(self):
        return self.__opc_conf


    @property
    def opc_version(self):
        return self.__opc_version


    @property
    def pmx_model_conf(self):
        return self.__pmx_model_conf


    @property
    def pressure_conf(self):
        return self.__pressure_conf


    @property
    def psu_conf(self):
        return self.__psu_conf


    @property
    def psu_version(self):
        return self.__psu_version


    @property
    def pt1000_calib(self):
        return self.__pt1000_calib


    @property
    def scd30_baseline(self):
        return self.__scd30_baseline


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
    def networks(self):
        return self.__networks


    @property
    def modem(self):
        return self.__modem


    @property
    def sim(self):
        return self.__sim


    @property
    def system_id(self):
        return self.__system_id


    @property
    def timezone_conf(self):
        return self.__timezone_conf


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Configuration:{hostname:%s, packs:%s, afe_baseline:%s, afe_id:%s, aws_api_auth:%s, " \
               "aws_group_config:%s, aws_project:%s, csv_logger_conf:%s, display_conf:%s, " \
               "vcal_baseline:%s, gas_baseline:%s, gas_model_conf:%s, gps_conf:%s, greengrass_identity:%s, " \
               "interface_conf:%s, mpl115a2_calib:%s, mqtt_conf:%s, ndir_conf:%s, opc_conf:%s, " \
               "opc_version:%s, pmx_model_conf:%s, pressure_conf:%s, psu_conf:%s, psu_version:%s, " \
               "pt1000_calib:%s,  scd30_baseline:%s, scd30_conf:%s, schedule:%s, shared_secret:%s, " \
               "sht_conf:%s, networks:%s,  modem:%s, sim:%s, system_id:%s, timezone_conf:%s}" % \
               (self.hostname, self.packs, self.afe_baseline, self.afe_id, self.aws_api_auth,
                self.aws_group_config, self.aws_project, self.csv_logger_conf, self.display_conf,
                self.vcal_baseline, self.gas_baseline, self.gas_model_conf, self.gps_conf, self.greengrass_identity,
                self.interface_conf, self.mpl115a2_calib, self.mqtt_conf, self.ndir_conf, self.opc_conf,
                self.opc_version, self.pmx_model_conf, self.pressure_conf, self.psu_conf, self.psu_version,
                self.pt1000_calib, self.scd30_baseline, self.scd30_conf, self.schedule, self.shared_secret,
                self.sht_conf, self.networks, self.modem, self.sim, self.system_id, self.timezone_conf)
