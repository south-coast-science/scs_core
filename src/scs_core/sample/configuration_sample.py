"""
Created on 23 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"rec": "2021-10-06T11:27:48Z", "tag": "scs-be2-3", "ver": 1.00, "val": {"hostname": "scs-bbe-003",
"packs": {"scs_comms": {"repo": "scs_comms_ge910", "version": null}, "scs_core": {"repo": "scs_core",
"version": "1.0.32"}, "scs_dev": {"repo": "scs_dev", "version": "1.0.11"}, "scs_dfe": {"repo": "scs_dfe_eng",
"version": "1.0.10"}, "scs_exegesis": {"repo": "scs_exegesis", "version": null},
"scs_greengrass": {"repo": "scs_greengrass", "version": "1.0.3"}, "scs_host": {"repo": "scs_host_bbe_southern",
"version": "1.0.6"}, "scs_inference": {"repo": "scs_inference", "version": null}, "scs_mfr": {"repo": "scs_mfr",
"version": "1.0.14"}, "scs_ndir": {"repo": "scs_ndir", "version": null},
"scs_psu": {"repo": "scs_psu", "version": "1.0.10"}},
"afe-baseline": {"sn1": {"calibrated-on": "2021-08-22T12:46:44Z", "offset": 13, "env": {"hmd": 62.6, "tmp": 24.5,
"pA": 102.1}}, "sn2": {"calibrated-on": "2021-08-22T12:46:38Z", "offset": -7, "env": {"hmd": 62.7, "tmp": 24.5,
"pA": 102.1}}, "sn3": {"calibrated-on": "2021-08-22T12:46:46Z", "offset": 24, "env": {"hmd": 62.6, "tmp": 24.5,
"pA": 102.1}}, "sn4": {"calibrated-on": "2021-08-22T12:46:41Z", "offset": 9, "env": {"hmd": 62.6, "tmp": 24.5,
"pA": 102.1}}}, "afe-id": {"serial_number": "27-000001", "type": "810-0023-02", "calibrated_on": "2016-11-01",
"sn1": {"serial_number": "212060308", "sensor_type": "NO2A43F"}, "sn2": {"serial_number": "132950202",
"sensor_type": "CO A4"}, "sn3": {"serial_number": "134060009", "sensor_type": "SO2A4"},
"sn4": {"serial_number": "133910023", "sensor_type": "H2SA4"}},
"aws-api-auth": {"endpoint": "aws.southcoastscience.com", "api-key": "a04c-62d684d64a1f"},
"aws-client-auth": {"endpoint": "asrfh6e5j5ecz.iot.us-west-2.amazonaws.com", "client-id": "scs-bbe-003",
"cert-id": "cd505d98bf"}, "aws-group-config": {"group-name": "scs-bbe-003-group",
"time-initiated": "2021-01-29T11:52:25Z", "unix-group": 987, "ml": true},
"aws-project": {"location-path": "south-coast-science-dev/development/loc/1",
"device-path": "south-coast-science-dev/development/device"},
"csv-logger-conf": {"root-path": "/srv/removable_data_storage", "delete-oldest": true, "write-interval": 0},
"display-conf": null, "gas-baseline": {"NO2": {"calibrated-on": "2021-08-22T12:40:13Z", "offset": 3,
"env": {"hmd": 62.5, "tmp": 24.3, "pA": 102.0}}}, "gas-model-conf": {"uds-path": "pipes/lambda-gas-model.uds",
"model-interface": "vB"}, "gps-conf": {"model": "SAM8Q", "sample-interval": 10, "tally": 60,
"report-file": "/tmp/southcoastscience/gps_report.json", "debug": false}, "interface-conf": {"model": "DFE"},
"greengrass-identity": null, "mpl115a2-calib": {"calibrated-on": "2020-11-15T11:29:23Z", "c25": 510},
"mqtt-conf": {"inhibit-publishing": true, "report-file": null, "debug": false}, "ndir-conf": {"model": "t1f1",
"tally": 1, "raw": false}, "opc-conf": {"model": "N3", "sample-period": 10, "restart-on-zeroes": true,
"power-saving": false}, "opc-version": null, "pmx-model-conf": {"uds-path": "pipes/lambda-pmx-model.uds",
"model-interface": "s1"}, "pressure-conf": {"model": "ICP", "altitude": 101}, "psu-conf": {"model": "OsloV1",
"batt-model": null, "ignore-threshold": false, "reporting-interval": 20,
"report-file": "/tmp/southcoastscience/psu_status_report.json"}, "psu-version": null,
"pt1000-calib": {"calibrated-on": "2017-08-15T11:21:45Z", "v20": 0.320208},
"scd30-baseline": {"CO2": {"calibrated-on": "2021-08-22T12:40:15Z", "offset": 5, "env": {"hmd": 62.5, "tmp": 24.3,
"pA": 102.0}}}, "scd30-conf": null, "schedule": {"scs-climate": {"interval": 60.0, "tally": 1},
"scs-gases": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}},
"shared-secret": {"key": "pYL7B1JcgJ2gy6MP"}, "sht-conf": {"int": "0x45", "ext": "0x45"},
"networks": {"eth0": {"kind": "ethernet", "state": "connected", "connection": "Ethernet eth0"},
"usb0": {"kind": "ethernet", "state": "unavailable", "connection": null}}, "modem": null, "sim": null,
"system-id": {"set-on": "2021-09-12T12:04:25Z", "vendor-id": "SCS", "model-id": "BE2", "model": "Alpha BB Eng",
"config": "V2", "system-sn": 3}, "timezone-conf": {"set-on": "2021-01-31T11:26:14Z", "name": "Europe/London"}}}
"""

import json

from collections import OrderedDict

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify, JSONable
from scs_core.data.path_dict import PathDict
from scs_core.data.str import Str

from scs_core.estate.configuration import Configuration

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationSample(Sample):
    """
    classdocs
    """

    __HIDDEN_VALUES = [
        'val.aws-api-auth.api-key',
        'val.shared-secret.key'
    ]


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        if not jdict:
            return None

        # Sample...
        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))

        try:
            version = round(float(jdict.get('ver')), 1)
        except (TypeError, ValueError):
            version = cls.DEFAULT_VERSION

        try:
            val_jdict = json.loads(jdict.get('val'))
        except TypeError:
            val_jdict = jdict.get('val')

        configuration = Configuration.construct_from_jdict(val_jdict)

        return cls(tag, rec, configuration, version=version)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, configuration, version=None):
        """
        Constructor
        """
        if version is None:
            version = Configuration.VERSION

        super().__init__(tag, rec, version)

        self.__configuration = configuration                # Configuration


    def __eq__(self, other):
        try:
            return self.tag == other.tag and self.configuration == other.configuration

        except (TypeError, AttributeError):
            return False


    def __lt__(self, other):
        if self.tag < other.tag:
            return True

        if self.tag > other.tag:
            return False

        if self.rec < other.rec:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def diff(self, other):
        return ConfigurationSample(self.tag, self.rec, self.configuration.diff(other.configuration))


    def as_table(self):
        path_dict = PathDict.construct_from_jstr(JSONify.dumps(self))
        rows = []

        for path in path_dict.paths():
            node = path_dict.node(path)
            value = '' if node is None else node

            key = path[4:] if path.startswith('val.') else path
            setting = '######' if path in self.__HIDDEN_VALUES else value

            rows.append(','.join((key, str(setting))))

        return rows


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def values(self):
        return self.configuration.as_json()


    @property
    def configuration(self):
        return self.__configuration


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationSample:{tag:%s, rec:%s, version:%s, configuration:%s}" % \
               (self.tag, self.rec, self.version, self.configuration)


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationSampleHistory(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, latest_only=False, items=None):
        """
        Constructor
        """
        self.__latest_only = latest_only                            # bool
        self.__items = {} if items is None else items               # dict of tag: list of ConfigurationSample


    # ----------------------------------------------------------------------------------------------------------------

    def insert(self, sample: ConfigurationSample):
        if sample.tag not in self.__items:
            self.__items[sample.tag] = []
            self.__items[sample.tag].append(sample)
            return

        if not self.__items[sample.tag] or not self.__latest_only:
            if sample not in self.__items[sample.tag]:            # we might not be reading all the fields in the DB!
                self.__items[sample.tag].append(sample)
            return

        for item in self.__items[sample.tag]:
            if sample.rec > item.rec:
                self.__items[sample.tag] = [sample]
                return


    # ----------------------------------------------------------------------------------------------------------------

    def diffs(self):
        diff_history = ConfigurationSampleHistory()

        for tag in self.tags():
            prev = None
            for item in self.items_for_tag(tag):
                diff_history.insert(item if prev is None else item.diff(prev))
                prev = item

        return diff_history


    def tags(self):
        return set(self.__items.keys())


    def items_for_tag(self, tag):
        if tag not in self.__items:
            return None

        return self.__items[tag]


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        items = []

        for tag in self.tags():
            items += self.items_for_tag(tag)

        return items


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationSampleHistory:{latest_only:%s, items:%s}" % \
               (self.__latest_only, Str.collection(self.__items))


# --------------------------------------------------------------------------------------------------------------------

class ConfigurationReport(ConfigurationSample):
    """
    classdocs
    """

    @classmethod
    def construct(cls, sample: ConfigurationSample, report: LocalizedDatetime):
        return cls(sample.tag, sample.rec, sample.configuration, report)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, configuration, report):
        """
        Constructor
        """
        super().__init__(tag, rec, configuration)

        self.__report = report                          # LocalizedDatetime


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['tag'] = self.tag
        jdict['rec'] = {'report': self.report.as_iso8601(), 'update': self.rec.as_iso8601()}
        jdict['ver'] = round(self.version, 1)

        jdict['val'] = self.values

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def report(self):
        return self.__report


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ConfigurationReport:{tag:%s, rec:%s, configuration:%s, report:%s}" % \
               (self.tag, self.rec, self.configuration, self.report)


