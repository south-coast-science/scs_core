"""
Created on 25 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://howchoo.com/g/ywi5m2vkodk/working-with-datetime-objects-and-timezones-in-python

example JSON:
{"path": "val.CO.cnc", "index": 0, "value": 340,
"sample": {"rec": "2021-07-30T19:45:00Z", "val": {
"NO2": {"weV": 0.31812, "cnc": 57.0, "aeV": 0.28576, "weC": 0.00323},
"Ox": {"weV": 0.41573, "cnc": 24.4, "aeV": 0.40003, "weC": 0.00181},
"NO": {"weV": 0.3081, "cnc": 34.9, "aeV": 0.28073, "weC": 0.05806},
"CO": {"weV": 0.35202, "cnc": 339.8, "aeV": 0.2881, "weC": 0.06908},
"sht": {"hmd": 69.9, "tmp": 18.5}}, "tag": "scs-bgx-401",
"exg": {"vB20": {"NO2": {"cnc": 14.4}}}}}
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.data.path_dict import PathDict

from scs_core.gas.a4.a4 import A4
from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.sensor_baseline import SensorBaseline, SensorBaselineSample


# --------------------------------------------------------------------------------------------------------------------

class Minimum(JSONable):
    """
    classdocs
    """

    FIELD_SELECTIONS = {'V': 'val.', 'E': 'exg.'}           # Val (model input) or Exg (model output)

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def init(cls):
        A4.init()


    @classmethod
    def find_minimums(cls, data, field_selection):
        if not data:
            return tuple()

        # minimums...
        field_group = cls.FIELD_SELECTIONS[field_selection]

        minimums = {path: None for path in PathDict(data[0]).paths()
                    if path.startswith(field_group) and (path.endswith('.cnc'))}    # or path.endswith('.vCal')

        # data...
        for i in range(len(data)):
            datum = PathDict(data[i])

            for path in minimums:
                value = round(float(datum.node(path)), 3)

                if minimums[path] is None or value < minimums[path].value:
                    minimums[path] = cls(path, i, value, data[i])

        return tuple(minimums[path] for path in sorted(minimums.keys()))


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, path, index, value, sample):
        """
        Constructor
        """
        self.__path = path                          # string
        self.__index = int(index)                   # int
        self.__value = round(value, 3)              # float
        self.__sample = sample                      # dict (of GasesSample)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['path'] = self.path
        jdict['index'] = self.index
        jdict['value'] = self.value
        jdict['sample'] = self.sample

        return jdict


    def summary(self, gas):
        sample = PathDict(self.sample)
        jdict = OrderedDict()

        jdict['rec'] = sample.node('rec')
        jdict[gas] = sample.node('.'.join(('val', gas)))
        jdict['sht'] = sample.node('val.sht')

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def update_already_done(self, configuration, end):
        cmd = self.__cmd()

        if cmd == 'scd30_baseline':
            baseline = configuration.scd30_baseline
            reported_baseline = None if baseline is None else baseline.sensor_baseline

        elif cmd == 'afe_baseline':
            baseline = AFEBaseline.null_datum() if configuration.afe_baseline is None else configuration.afe_baseline
            reported_baseline = baseline.sensor_baseline(configuration.afe_id.sensor_index(self.gas))

        elif cmd == 'vcal_baseline':
            baseline = configuration.vcal_baseline
            reported_baseline = None if baseline is None else baseline.sensor_baseline(self.gas)

        elif cmd == 'gas_baseline':
            baseline = configuration.gas_baseline
            reported_baseline = None if baseline is None else baseline.sensor_baseline(self.gas)

        else:
            raise ValueError(cmd)

        sensor_baseline = SensorBaseline.null_datum() if reported_baseline is None else reported_baseline

        return sensor_baseline.calibrated_on is not None and sensor_baseline.calibrated_on > end


    def cmd_tokens(self, conf_minimums):
        cmd = self.__cmd()
        value = int(round(self.value))
        sample = SensorBaselineSample.construct_from_sample_jdict(self.sample)      # TODO: sample needs pressure!

        if cmd == 'scd30_baseline':
            return (cmd, '-vc', conf_minimums[self.gas], value,
                    '-t', sample.temp, '-m', sample.humid)          # , '-p', sample.press

        if cmd == 'afe_baseline':
            return (cmd, '-vc', self.gas, conf_minimums[self.gas], value,
                    '-r', sample.rec.as_iso8601(), '-t', sample.temp, '-m', sample.humid)

        # hueristics:
        # NO2 - make minimum value 10
        # SO2 - make minimum value -20

        if cmd == 'vcal_baseline':                  # set vCal offset to make minimum value 0
            return (cmd, '-vs', self.gas, -value,
                    '-r', sample.rec.as_iso8601(), '-t', sample.temp, '-m', sample.humid)

        if cmd == 'gas_baseline':
            return (cmd, '-vc', self.gas, conf_minimums[self.gas], value,
                    '-r', sample.rec.as_iso8601(), '-t', sample.temp, '-m', sample.humid)

        raise ValueError(cmd)


    # ----------------------------------------------------------------------------------------------------------------

    def __cmd(self):
        if self.gas == 'CO2':
            return 'scd30_baseline'

        if self.source == 'val' and self.interpretation == 'cnc':
            return 'afe_baseline'

        if self.source == 'val' and self.interpretation == 'vCal':
            return 'vcal_baseline'

        if self.source == 'exg':
            return 'gas_baseline'

        raise ValueError(self.source)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def source(self):
        return self.__path.split('.')[0]


    @property
    def interpretation(self):
        return self.__path.split('.')[-1]


    @property
    def gas(self):
        return self.__path.split('.')[-2]


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def path(self):
        return self.__path


    @property
    def index(self):
        return self.__index


    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = round(value, 3)


    @property
    def sample(self):
        return self.__sample


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Minimum:{path:%s, index:%s, value:%s, sample:%s}" % \
               (self.path, self.index, self.value, self.sample)
