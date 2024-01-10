"""
Created on 27 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

    VERSION = 1.3

example document:
{
    "rec": "2024-01-10T12:47:17Z",
    "tag": "scs-be2-3",
    "ver": 1.4,
    "val": {
        "hostname": "scs-bbe-003",
        "os": {
            "rel": "6.1.38-bone21"
        },
        "packs": {
            "scs_comms": {
                "repo": "scs_comms_ge910",
                "version": null
            },
            "scs_core": {
                "repo": "scs_core",
                "version": "3.6.0"
            },
            "scs_dev": {
                "repo": "scs_dev",
                "version": "3.2.3"
            },
            "scs_dfe": {
                "repo": "scs_dfe_eng",
                "version": "3.0.0"
            },
            "scs_exegesis": {
                "repo": "scs_exegesis",
                "version": null
            },
            "scs_host": {
                "repo": "scs_host_bbe_southern",
                "version": "3.4.2"
            },
            "scs_inference": {
                "repo": "scs_inference",
                "version": null
            },
            "scs_mfr": {
                "repo": "scs_mfr",
                "version": "3.6.1"
            },
            "scs_ndir": {
                "repo": "scs_ndir",
                "version": null
            },
            "scs_psu": {
                "repo": "scs_psu",
                "version": "2.5.2"
            }
        },
        "afe-baseline": {
            "sn1": {
                "calibrated-on": "2023-12-07T12:43:55Z",
                "offset": 0
            },
            "sn2": {
                "calibrated-on": "2023-12-07T12:43:55Z",
                "offset": 0
            },
            "sn3": {
                "calibrated-on": "2023-12-07T12:43:55Z",
                "offset": 0
            },
            "sn4": {
                "calibrated-on": "2023-12-07T12:43:55Z",
                "offset": 0
            }
        },
        "afe-id": {
            "serial_number": "26-000345",
            "type": "810-0023-01",
            "calibrated_on": "2020-11-18",
            "sn1": {
                "serial_number": "212632052",
                "sensor_type": "NO2A43F"
            },
            "sn2": {
                "serial_number": "214250436",
                "sensor_type": "OXA431"
            },
            "sn3": {
                "serial_number": "130631043",
                "sensor_type": "NO A4"
            },
            "sn4": {
                "serial_number": "134200204",
                "sensor_type": "SO2A4"
            }
        },
        "aws-group-config": {
            "group-name": "scs-bbe-003-group",
            "time-initiated": "2023-12-22T10:26:28Z",
            "unix-group": 987,
            "ml": "uE.1"
        },
        "aws-project": {
            "location-path": "south-coast-science-dev/development/loc/1",
            "device-path": "south-coast-science-dev/development/device"
        },
        "data-log": {
            "path": "/srv/removable_data_storage",
            "is-available": true,
            "on-root": false,
            "used": 6
        },
        "display-conf": null,
        "vcal-baseline": null,
        "gas-baseline": null,
        "gas-model-conf": {
            "uds-path": "pipes/lambda-gas-model.uds",
            "model-interface": "vE",
            "model-compendium-group": "uE.1"
        },
        "gps-conf": {
            "model": "SAM8Q",
            "sample-interval": 10,
            "tally": 60,
            "report-file": "/tmp/southcoastscience/gps_report.json",
            "debug": false
        },
        "interface-conf": {
            "model": "DFE"
        },
        "mpl115a2-calib": null,
        "opc-conf": {
            "model": "N3",
            "sample-period": 10,
            "restart-on-zeroes": true,
            "power-saving": false
        },
        "opc-version": {
            "serial": "177050912",
            "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"
        },
        "opc-errors": 1,
        "pmx-model-conf": {
            "uds-path": "pipes/lambda-pmx-model.uds",
            "model-interface": "s2"
        },
        "pressure-conf": null,
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
        "sht-conf": {
            "int": "0x45",
            "ext": "0x45"
        },
        "networks": null,
        "modem": {
            "id": "992c3ac6da0b68d58005d20ea5e957d409001e42",
            "imei": "860425041573914",
            "mfr": "QUALCOMM INCORPORATED",
            "model": "QUECTEL Mobile Broadband Module",
            "rev": "EC25ECGAR06A05M1G"
        },
        "sim": {
            "imsi": "234301951432537",
            "iccid": "8944303382697124823",
            "operator-code": "23430",
            "operator-name": "EE"
        },
        "system-id": {
            "set-on": "2024-01-09T16:02:09Z",
            "vendor-id": "SCS",
            "model-id": "BE2",
            "model": "Alpha BB Eng",
            "config": "V2",
            "system-sn": 3
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

from scs_core.csv.csv_logger_conf import CSVLoggerConf

from scs_core.data.json import JSONable

from scs_core.display.display_conf import DisplayConf

from scs_core.estate.package_version import PackageVersions

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.afe_id import AFEId
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
from scs_core.particulate.opc_error_log import OPCErrorSummary
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

    VERSION = 1.4

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
                           None)
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
        opc_conf = OPCConf.construct_from_jdict(jdict.get('opc-conf'))
        opc_version = OPCVersion.construct_from_jdict(jdict.get('opc-version'))
        opc_error_summary = OPCErrorSummary.construct_from_jdict(jdict.get('opc-errors'))
        pmx_model_conf = PMxModelConf.construct_from_jdict(jdict.get('pmx-model-conf'))
        pressure_conf = PressureConf.construct_from_jdict(jdict.get('pressure-conf'))
        psu_conf = PSUConf.construct_from_jdict(jdict.get('psu-conf'))
        psu_version = PSUVersion.construct_from_jdict(jdict.get('psu-version'))
        scd30_baseline = SCD30Baseline.construct_from_jdict(jdict.get('scd30-baseline'))
        scd30_conf = SCD30Conf.construct_from_jdict(jdict.get('scd30-conf'))
        schedule = Schedule.construct_from_jdict(jdict.get('schedule'))
        sht_conf = SHTConf.construct_from_jdict(jdict.get('sht-conf'))
        networks = Networks.construct_from_jdict(jdict.get('networks'))
        modem = Modem.construct_from_jdict(jdict.get('modem'))
        sim = SIM.construct_from_jdict(jdict.get('sim'))
        system_id = SystemID.construct_from_jdict(jdict.get('system-id'))
        timezone_conf = TimezoneConf.construct_from_jdict(jdict.get('timezone-conf'))

        return cls(hostname, platform, packs, afe_baseline, afe_id,
                   aws_group_config, aws_project, data_log, display_conf, vcal_baseline,
                   gas_baseline, gas_model_conf, gps_conf, interface_conf, mpl115a2_calib,
                   opc_conf, opc_version, opc_error_summary, pmx_model_conf, pressure_conf,
                   psu_conf, psu_version, scd30_baseline, scd30_conf, schedule,
                   sht_conf, networks, modem, sim, system_id,
                   timezone_conf)


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
        opc_conf = OPCConf.load(manager)
        opc_version = OPCVersion.load(manager)
        opc_error_summary = OPCErrorSummary.load(manager)
        pmx_model_conf = PMxModelConf.load(manager)
        pressure_conf = PressureConf.load(manager)
        psu_conf = PSUConf.load(manager)
        psu_version = psu_version
        scd30_baseline = SCD30Baseline.load(manager)
        scd30_conf = SCD30Conf.load(manager)
        schedule = Schedule.load(manager)
        sht_conf = SHTConf.load(manager)
        networks = None                                         # now provided by Status class
        modem = manager.modem()
        sim = None if exclude_sim else manager.sim()
        system_id = SystemID.load(manager)
        timezone_conf = TimezoneConf.load(manager)

        return cls(hostname, platform, packs, afe_baseline, afe_id,
                   aws_group_config, aws_project, data_log, display_conf, vcal_baseline,
                   gas_baseline, gas_model_conf, gps_conf, interface_conf, mpl115a2_calib,
                   opc_conf, opc_version, opc_error_summary, pmx_model_conf, pressure_conf,
                   psu_conf, psu_version, scd30_baseline, scd30_conf, schedule,
                   sht_conf, networks, modem, sim, system_id,
                   timezone_conf)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, hostname, platform, packs, afe_baseline, afe_id,
                 aws_group_config, aws_project, data_log, display_conf, vcal_baseline,
                 gas_baseline, gas_model_conf, gps_conf, interface_conf, mpl115a2_calib,
                 opc_conf, opc_version, opc_error_summary, pmx_model_conf, pressure_conf,
                 psu_conf, psu_version, scd30_baseline, scd30_conf, schedule,
                 sht_conf, networks, modem, sim, system_id,
                 timezone_conf):
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
        self.__opc_conf = opc_conf                                  # OPCConf
        self.__opc_version = opc_version                            # OPCVersion
        self.__opc_error_summary = opc_error_summary                # OPCErrorSummary
        self.__pmx_model_conf = pmx_model_conf                      # PMxModelConf
        self.__pressure_conf = pressure_conf                        # PressureConf
        self.__psu_conf = psu_conf                                  # PSUConf
        self.__psu_version = psu_version                            # PSUVersion
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
                self.opc_conf == other.opc_conf and self.opc_version == other.opc_version and \
                self.opc_error_summary == other.opc_error_summary and self.pmx_model_conf == other.pmx_model_conf and \
                self.pressure_conf == other.pressure_conf and self.psu_conf == other.psu_conf and \
                self.psu_version == other.psu_version and self.scd30_baseline == other.scd30_baseline and \
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
                             None)

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

        if self.opc_conf:
            self.opc_conf.save(manager)

        if self.opc_version:
            raise ValueError('opc_version may not be set')

        if self.opc_error_summary:
            raise ValueError('opc_error_summary may not be set')

        if self.pmx_model_conf:
            self.pmx_model_conf.save(manager)

        if self.pressure_conf:
            self.pressure_conf.save(manager)

        if self.psu_conf:
            self.psu_conf.save(manager)

        if self.psu_version:
            raise ValueError('psu_version may not be set')

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
        jdict['opc-conf'] = self.opc_conf
        jdict['opc-version'] = self.opc_version
        jdict['opc-errors'] = self.opc_error_summary
        jdict['pmx-model-conf'] = self.pmx_model_conf
        jdict['pressure-conf'] = self.pressure_conf
        jdict['psu-conf'] = self.psu_conf
        jdict['psu-version'] = self.psu_version
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
    def opc_conf(self):
        return self.__opc_conf


    @property
    def opc_version(self):
        return self.__opc_version


    @property
    def opc_error_summary(self):
        return self.__opc_error_summary


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
        return "Configuration:{hostname:%s, platform:%s, packs:%s, afe_baseline:%s, afe_id:%s, " \
               "aws_group_config:%s, aws_project:%s, data_log:%s, display_conf:%s, vcal_baseline:%s, " \
               "gas_baseline:%s, gas_model_conf:%s, gps_conf:%s, interface_conf:%s, mpl115a2_calib:%s, " \
               "opc_conf:%s, opc_version:%s, opc_error_summary:%s, pmx_model_conf:%s, pressure_conf:%s, " \
               "psu_conf:%s, psu_version:%s, scd30_baseline:%s, scd30_conf:%s, schedule:%s, " \
               "sht_conf:%s, networks:%s, modem:%s, sim:%s, system_id:%s, " \
               "timezone_conf:%s}" % \
               (self.hostname, self.platform, self.packs, self.afe_baseline, self.afe_id,
                self.aws_group_config, self.aws_project, self.data_log, self.display_conf, self.vcal_baseline,
                self.gas_baseline, self.gas_model_conf, self.gps_conf, self.interface_conf, self.mpl115a2_calib,
                self.opc_conf, self.opc_version, self.opc_error_summary, self.pmx_model_conf, self.pressure_conf,
                self.psu_conf, self.psu_version, self.scd30_baseline, self.scd30_conf, self.schedule,
                self.sht_conf, self.networks, self.modem, self.sim, self.system_id,
                self.timezone_conf)
