"""
Created on 27 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

    VERSION = 1.3

example document:
{
    "rec": "2023-02-28T12:25:24Z",
    "tag": "scs-bgx-431",
    "ver": 1.3,
    "val": {
        "hostname": "scs-bbe-431",
        "os": {
            "rel": "4.19.173-bone60",
            "vers": "#1buster PREEMPT Tue Feb 16 23:42:12 UTC 2021"
        },
        "packs": {
            "scs_core": {
                "repo": "scs_core",
                "version": "2.4.1"
            },
            "scs_dev": {
                "repo": "scs_dev",
                "version": "2.4.0"
            },
            "scs_dfe": {
                "repo": "scs_dfe_eng",
                "version": "2.4.0"
            },
            "scs_greengrass": {
                "repo": "scs_greengrass",
                "version": "2.4.0"
            },
            "scs_host": {
                "repo": "scs_host_bbe_southern",
                "version": "1.0.13"
            },
            "scs_mfr": {
                "repo": "scs_mfr",
                "version": "1.5.4"
            },
            "scs_psu": {
                "repo": "scs_psu",
                "version": "1.2.0"
            }
        },
        "afe-baseline": {
            "sn1": {
                "calibrated-on": "2023-02-08T12:52:39Z",
                "offset": 10,
                "env": {
                    "rec": "2023-02-08T02:40:00Z",
                    "hmd": 30.7,
                    "tmp": 20.3
                }
            },
            "sn2": {
                "calibrated-on": "2023-02-08T12:52:42Z",
                "offset": 48,
                "env": {
                    "rec": "2023-02-08T07:55:00Z",
                    "hmd": 31.3,
                    "tmp": 19.5
                }
            },
            "sn3": {
                "calibrated-on": "2023-02-08T12:52:37Z",
                "offset": 97,
                "env": {
                    "rec": "2023-02-07T17:05:00Z",
                    "hmd": 31.7,
                    "tmp": 23.1
                }
            },
            "sn4": {
                "calibrated-on": "2023-02-08T12:52:32Z",
                "offset": 142,
                "env": {
                    "rec": "2023-02-08T05:45:00Z",
                    "hmd": 31.0,
                    "tmp": 19.8
                }
            }
        },
        "afe-id": {
            "serial_number": "26-000595",
            "type": "810-0023-01",
            "calibrated_on": "2022-11-23",
            "sn1": {
                "serial_number": "212801359",
                "sensor_type": "NO2A43F"
            },
            "sn2": {
                "serial_number": "214801144",
                "sensor_type": "OXA431"
            },
            "sn3": {
                "serial_number": "130820459",
                "sensor_type": "NO A4"
            },
            "sn4": {
                "serial_number": "132800043",
                "sensor_type": "CO A4"
            }
        },
        "aws-group-config": {
            "group-name": "scs-bbe-431-group",
            "time-initiated": "2023-02-28T10:32:28Z",
            "unix-group": 987,
            "ml": "uE.1"
        },
        "aws-project": {
            "location-path": "ricardo/heathrow/loc/4",
            "device-path": "ricardo/heathrow/device"
        },
        "data-log": {
            "path": "/srv/removable_data_storage",
            "is-available": true,
            "on-root": false,
            "used": 6
        },
        "display-conf": null,
        "vcal-baseline": {
            "NO": {
                "calibrated-on": "2023-01-22T18:56:44Z",
                "offset": -15
            },
            "NO2": {
                "calibrated-on": "2023-01-22T08:45:53Z",
                "offset": 2
            }
        },
        "gas-baseline": null,
        "gas-model-conf": {
            "uds-path": "pipes/lambda-gas-model.uds",
            "model-interface": "vE",
            "model-compendium-group": "uE.1"
        },
        "gps-conf": {
            "model": "PAM7Q",
            "sample-interval": 10,
            "tally": 60,
            "report-file": "/tmp/southcoastscience/gps_report.json",
            "debug": false
        },
        "interface-conf": null,
        "mpl115a2-calib": {
            "calibrated-on": "2021-03-18T13:25:10Z",
            "c25": 506
        },
        "mqtt-conf": {
            "inhibit-publishing": false,
            "report-file": null,
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
            "serial": "177780318",
            "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"
        },
        "pmx-model-conf": {
            "uds-path": "pipes/lambda-pmx-model.uds",
            "model-interface": "s2"
        },
        "pressure-conf": {
            "model": "ICP",
            "altitude": 25
        },
        "psu-conf": {
            "model": "OsloV1",
            "batt-model": null,
            "ignore-threshold": false,
            "reporting-interval": 10,
            "report-file": "/tmp/southcoastscience/psu_status_report.json"
        },
        "psu-version": {
            "id": "South Coast Science PSU Oslo",
            "tag": "2.2.5"
        },
        "pt1000-calib": {
            "calibrated-on": "2017-08-15T11:21:45Z",
            "v20": 0.320208
        },
        "scd30-baseline": {
            "CO2": {
                "calibrated-on": "2023-02-08T12:52:34Z",
                "offset": -7,
                "env": {
                    "hmd": 30.9,
                    "tmp": 20.0
                }
            }
        },
        "scd30-conf": {
            "sample-interval": 5,
            "temp-offset": 0.0
        },
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
        "sht-conf": {
            "int": "0x45",
            "ext": "0x45"
        },
        "networks": {
            "cdc-wdm0": {
                "kind": "gsm",
                "state": "connected",
                "connection": "EE M2M"
            },
            "eth0": {
                "kind": "ethernet",
                "state": "unavailable",
                "connection": null
            }
        },
        "modem": {
            "id": "e3f0ca1c3134d586a9c47dc4fd6c1cb46e6",
            "imei": "866758042325619",
            "mfr": "QUALCOMM INCORPORATED",
            "model": "QUECTEL Mobile Broadband Module",
            "rev": "EC2506A03M4G"
        },
        "sim": {
            "imsi": "234301951432536",
            "iccid": "8944303382697124815",
            "operator-code": "23430",
            "operator-name": "EE"
        },
        "system-id": {
            "set-on": "2019-01-04T11:28:27Z",
            "vendor-id": "SCS",
            "model-id": "BGX",
            "model": "Praxis",
            "config": "BGX",
            "system-sn": 431
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

from scs_core.aws.config.project import Project
from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration

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

from scs_core.sys.filesystem import FilesystemReport
from scs_core.sys.modem import Modem, SIM
from scs_core.sys.network import Networks
from scs_core.sys.platform import PlatformSummary
from scs_core.sys.system_id import SystemID


# --------------------------------------------------------------------------------------------------------------------

class Configuration(JSONable):
    """
    classdocs
    """

    VERSION = 1.3

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
                           None, None, None)
            else:
                return None

        hostname = jdict.get('hostname')
        platform = PlatformSummary.construct_from_jdict(jdict.get('os'))
        packs = PackageVersions.construct_from_jdict(jdict.get('packs'))

        afe_baseline = AFEBaseline.construct_from_jdict(jdict.get('afe-baseline'))
        afe_id = AFEId.construct_from_jdict(jdict.get('afe-id'))
        aws_group_config = AWSGroupConfiguration.construct_from_jdict(jdict.get('aws-group-config'))
        aws_project = Project.construct_from_jdict(jdict.get('aws-project'))
        data_log = FilesystemReport.construct_from_jdict(jdict.get('data-log'))
        display_conf = DisplayConf.construct_from_jdict(jdict.get('display-conf'))
        vcal_baseline = VCalBaseline.construct_from_jdict(jdict.get('vcal-baseline'))
        gas_baseline = GasBaseline.construct_from_jdict(jdict.get('gas-baseline'))
        gas_model_conf = GasModelConf.construct_from_jdict(jdict.get('gas-model-conf'))
        gps_conf = GPSConf.construct_from_jdict(jdict.get('gps-conf'))
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
        sht_conf = SHTConf.construct_from_jdict(jdict.get('sht-conf'))
        networks = Networks.construct_from_jdict(jdict.get('networks'))
        modem = Modem.construct_from_jdict(jdict.get('modem'))
        sim = SIM.construct_from_jdict(jdict.get('sim'))
        system_id = SystemID.construct_from_jdict(jdict.get('system-id'))
        timezone_conf = TimezoneConf.construct_from_jdict(jdict.get('timezone-conf'))

        return cls(hostname, platform, packs, afe_baseline, afe_id, aws_group_config,
                   aws_project, data_log, display_conf, vcal_baseline, gas_baseline,
                   gas_model_conf, gps_conf, interface_conf, mpl115a2_calib,
                   mqtt_conf, ndir_conf, opc_conf, opc_version, pmx_model_conf,
                   pressure_conf, psu_conf, psu_version, pt1000_calib, scd30_baseline,
                   scd30_conf, schedule, sht_conf, networks, modem,
                   sim, system_id, timezone_conf)


    @classmethod
    def load(cls, manager, psu_version=None, exclude_sim=False):
        csv_logger_conf = CSVLoggerConf.load(manager)

        hostname = socket.gethostname()
        platform = PlatformSummary.construct()
        packs = PackageVersions.construct_from_installation(manager.scs_path(), manager)

        afe_baseline = AFEBaseline.load(manager)
        afe_id = AFEId.load(manager)
        aws_group_config = AWSGroupConfiguration.load(manager)
        aws_project = Project.load(manager)
        data_log = None if csv_logger_conf is None else csv_logger_conf.filesystem_report()
        display_conf = DisplayConf.load(manager)
        vcal_baseline = VCalBaseline.load(manager)
        gas_baseline = GasBaseline.load(manager)
        gas_model_conf = GasModelConf.load(manager)
        gps_conf = GPSConf.load(manager)
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
        sht_conf = SHTConf.load(manager)
        networks = None                                         # now provided by Status class
        modem = manager.modem()
        sim = None if exclude_sim else manager.sim()
        system_id = SystemID.load(manager)
        timezone_conf = TimezoneConf.load(manager)

        return cls(hostname, platform, packs, afe_baseline, afe_id, aws_group_config,
                   aws_project, data_log, display_conf, vcal_baseline, gas_baseline,
                   gas_model_conf, gps_conf, interface_conf, mpl115a2_calib,
                   mqtt_conf, ndir_conf, opc_conf, opc_version, pmx_model_conf,
                   pressure_conf, psu_conf, psu_version, pt1000_calib, scd30_baseline,
                   scd30_conf, schedule, sht_conf, networks, modem,
                   sim, system_id, timezone_conf)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, hostname, platform, packs, afe_baseline, afe_id, aws_group_config,
                 aws_project, data_log, display_conf, vcal_baseline, gas_baseline,
                 gas_model_conf, gps_conf, interface_conf, mpl115a2_calib,
                 mqtt_conf, ndir_conf, opc_conf, opc_version, pmx_model_conf,
                 pressure_conf, psu_conf, psu_version, pt1000_calib, scd30_baseline,
                 scd30_conf, schedule, sht_conf, networks, modem,
                 sim, system_id, timezone_conf):
        """
        Constructor
        """

        self.__hostname = hostname                                  # string
        self.__platform = platform                                  # PlatformSummary
        self.__packs = packs                                        # PackageVersions

        self.__afe_baseline = afe_baseline                          # AFEBaseline
        self.__afe_id = afe_id                                      # AFEId
        self.__aws_group_config = aws_group_config                  # AWSGroupConfiguration
        self.__aws_project = aws_project                            # Project
        self.__data_log = data_log                                  # FilesystemReport
        self.__display_conf = display_conf                          # DisplayConf
        self.__vcal_baseline = vcal_baseline                        # VCalBaseline
        self.__gas_baseline = gas_baseline                          # GasBaseline
        self.__gas_model_conf = gas_model_conf                      # GasModelConf
        self.__gps_conf = gps_conf                                  # GPSConf
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
        self.__sht_conf = sht_conf                                  # SHTConf
        self.__networks = networks                                  # Networks or None
        self.__modem = modem                                        # Modem
        self.__sim = sim                                            # SIM
        self.__system_id = system_id                                # SystemID
        self.__timezone_conf = timezone_conf                        # TimezoneConf


    def __eq__(self, other):
        try:
            return self.hostname == other.hostname and self.platform == other.platform and \
                   self.packs == other.packs and self.afe_baseline == other.afe_baseline and \
                   self.afe_id == other.afe_id and self.aws_project == other.aws_project and \
                   self.data_log == other.data_log and self.display_conf == other.display_conf and \
                   self.vcal_baseline == other.vcal_baseline and self.gas_baseline == other.gas_baseline and \
                   self.gas_model_conf == other.gas_model_conf and self.gps_conf == other.gps_conf and \
                   self.interface_conf == other.interface_conf and self.mpl115a2_calib == other.mpl115a2_calib and \
                   self.mqtt_conf == other.mqtt_conf and self.ndir_conf == other.ndir_conf and \
                   self.opc_conf == other.opc_conf and self.pmx_model_conf == other.pmx_model_conf and \
                   self.pmx_model_conf == other.pmx_model_conf and self.pressure_conf == other.pressure_conf and \
                   self.psu_conf == other.psu_conf and self.psu_version == other.psu_version and \
                   self.pt1000_calib == other.pt1000_calib and self.scd30_baseline == other.scd30_baseline and \
                   self.scd30_conf == other.scd30_conf and self.schedule == other.schedule and \
                   self.sht_conf == other.sht_conf and self.networks == other.networks and \
                   self.modem == other.modem and self.sim == other.sim and \
                   self.system_id == other.system_id and self.timezone_conf == other.timezone_conf

        except (TypeError, AttributeError):
            return False


    def diff(self, other):
        diff = Configuration(None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None, None, None,
                             None, None, None)

        if self.hostname != other.hostname:
            diff.__hostname = self.hostname

        if self.platform != other.platform:
            diff.__platform = self.platform

        if self.packs != other.packs:
            diff.__packs = self.packs

        if self.afe_id != other.afe_id:
            diff.__afe_id = self.afe_id

        if self.aws_group_config != other.aws_group_config:
            diff.__aws_group_config = self.aws_group_config

        if self.aws_project != other.aws_project:
            diff.__aws_project = self.aws_project

        if self.data_log != other.data_log:
            diff.__data_log = self.data_log

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

        if self.platform:
            raise ValueError('platform may not be set')

        if self.packs:
            raise ValueError('packs may not be set')

        if self.afe_baseline:
            self.afe_baseline.save(manager)

        if self.afe_id:
            raise ValueError('afe_id may not be set')

        if self.aws_group_config:
            self.aws_group_config.save(manager)

        if self.aws_project:
            self.aws_project.save(manager)

        if self.data_log:
            raise ValueError('data_log may not be set')

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
        jdict['os'] = self.platform
        jdict['packs'] = self.packs

        jdict['afe-baseline'] = self.afe_baseline
        jdict['afe-id'] = self.afe_id
        jdict['aws-group-config'] = self.aws_group_config
        jdict['aws-project'] = self.aws_project
        jdict['data-log'] = self.data_log
        jdict['display-conf'] = self.display_conf
        jdict['vcal-baseline'] = self.vcal_baseline
        jdict['gas-baseline'] = self.gas_baseline
        jdict['gas-model-conf'] = self.gas_model_conf
        jdict['gps-conf'] = self.gps_conf
        jdict['interface-conf'] = self.interface_conf
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
    def platform(self):
        return self.__platform


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
    def aws_group_config(self):
        return self.__aws_group_config


    @property
    def aws_project(self):
        return self.__aws_project


    @property
    def data_log(self):
        return self.__data_log


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
        return "Configuration:{hostname:%s, platform:%s, packs:%s, afe_baseline:%s, afe_id:%s, aws_group_config:%s, " \
               "aws_project:%s, data_log:%s, display_conf:%s, vcal_baseline:%s, gas_baseline:%s, " \
               "gas_model_conf:%s, gps_conf:%s, interface_conf:%s, mpl115a2_calib:%s, " \
               "mqtt_conf:%s, ndir_conf:%s, opc_conf:%s, opc_version:%s, pmx_model_conf:%s, " \
               "pressure_conf:%s, psu_conf:%s, psu_version:%s, pt1000_calib:%s, scd30_baseline:%s, " \
               "scd30_conf:%s, schedule:%s, sht_conf:%s, networks:%s, modem:%s, " \
               "sim:%s, system_id:%s, timezone_conf:%s}" % \
               (self.hostname, self.platform, self.packs, self.afe_baseline, self.afe_id, self.aws_group_config,
                self.aws_project, self.data_log, self.display_conf, self.vcal_baseline, self.gas_baseline,
                self.gas_model_conf, self.gps_conf, self.interface_conf, self.mpl115a2_calib,
                self.mqtt_conf, self.ndir_conf, self.opc_conf, self.opc_version, self.pmx_model_conf,
                self.pressure_conf, self.psu_conf, self.psu_version, self.pt1000_calib, self.scd30_baseline,
                self.scd30_conf, self.schedule, self.sht_conf, self.networks, self.modem,
                self.sim, self.system_id, self.timezone_conf)
