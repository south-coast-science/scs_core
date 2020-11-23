"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"tag": "scs-be2-2",
 "rec": "2017-09-24T07:51:21Z",
 "val": {
  "NO2": {"weV": 0.312317, "aeV": 0.31038, "weC": -0.001, "cnc": 14.8},
  "CO": {"weV": 0.325005, "aeV": 0.254254, "weC": 0.077239, "cnc": 323.2},
  "SO2": {"weV": 0.277942, "aeV": 0.267754, "weC": 0.004136, "cnc": 27.6},
  "H2S": {"weV": 0.221816, "aeV": 0.269817, "weC": -0.006301, "cnc": 29.6},
  "pt1": {"v": 0.321411, "tmp": 21.9},
  "sht": {"hmd": 73.0, "tmp": 21.4}}}
"""

from collections import OrderedDict

from scs_core.climate.sht_datum import SHTDatum

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.str import Str

from scs_core.gas.a4.a4_datum import A4Datum
from scs_core.gas.afe.afe_datum import AFEDatum
from scs_core.gas.afe.pt1000_datum import Pt1000Datum
from scs_core.gas.pid.pid import PIDDatum
from scs_core.gas.scd30.scd30_datum import SCD30Datum

from scs_core.sample.sample import Sample


# TODO: get src from AFE / ISI datum?

# --------------------------------------------------------------------------------------------------------------------

class GasesSample(Sample):
    """
    classdocs
    """

    __NON_ELECTROCHEM_FIELDS = ['pt1', 'sht', 'CO2', 'VOC']
    __VOC_FIELDS = ['VOC']

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # Sample...
        tag = jdict.get('tag')
        rec = LocalizedDatetime.construct_from_jdict(jdict.get('rec'))
        val = jdict.get('val')
        exegeses = jdict.get('exg')

        # GasesSample...
        node = val.get('pt1')
        pt1000_datum = None if node is None else Pt1000Datum(node.get('v'), temp=node.get('tmp'))

        node = val.get('sht')
        sht_datum = SHTDatum(node.get('hmd'), node.get('tmp'))

        node = val.get('CO2')
        scd30_datum = None if node is None else SCD30Datum(node.get('cnc'), None, None)

        sns = OrderedDict()

        for field, node in val.items():
            if field not in cls.__NON_ELECTROCHEM_FIELDS:
                sns[field] = A4Datum.construct_from_jdict(node)

            if field in cls.__VOC_FIELDS:
                sns[field] = PIDDatum.construct_from_jdict(node)

        electrochem_datum = AFEDatum(pt1000_datum, *list(sns.items()))

        return cls(tag, rec, scd30_datum, electrochem_datum, sht_datum, exegeses=exegeses)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, scd30_datum, electrochem_datum, sht_datum, exegeses=None):
        """
        Constructor
        """
        super().__init__(tag, rec, exegeses=exegeses)

        self.__scd30_datum = scd30_datum                            # SCD30Datum
        self.__electrochem_datum = electrochem_datum                # AFEDatum or ISIDatum
        self.__sht_datum = sht_datum                                # SHT31Datum


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def has_invalid_value(cls):
        # TODO: implement has_invalid_value
        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def values(self):
        jdict = OrderedDict()

        if self.scd30_datum is not None:
            jdict['CO2'] = {'cnc': self.scd30_datum.co2}

        if self.electrochem_datum is not None:
            for key, value in self.electrochem_datum.sns.items():
                jdict[key] = value.as_json()

            try:
                if self.electrochem_datum.pt1000 is not None:
                    jdict['pt1'] = self.electrochem_datum.pt1000.as_json()
            except AttributeError:
                pass

        if self.sht_datum is not None:
            jdict['sht'] = self.sht_datum.as_json()

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def scd30_datum(self):
        return self.__scd30_datum


    @property
    def electrochem_datum(self):
        return self.__electrochem_datum


    @property
    def sht_datum(self):
        return self.__sht_datum


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        exegeses = Str.collection(self.exegeses)

        return "GasesSample:{tag:%s, rec:%s, exegeses:%s, scd30_datum:%s, electrochem_datum:%s, sht_datum:%s}" % \
            (self.tag, self.rec, exegeses, self.scd30_datum, self.electrochem_datum, self.sht_datum)
