"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"rec": "2021-10-11T10:59:40Z", "tag": "scs-be2-3", "ver": 2.0, "src": "AFE",
"val": {"NO2": {"weV": 0.29057, "aeV": 0.29544, "weC": 0.00131, "cnc": 20.9, "vCal": 15.41},
"Ox": {"weV": 0.40101, "aeV": 0.39969, "weC": 0.00235, "cnc": 55.7, "vCal": 6.61, "xCal": -0.390731},
"CO": {"weV": 0.44069, "aeV": 0.30213, "weC": 0.16795, "cnc": 685.4, "vCal": 562.256},
"sht": {"hmd": 52.9, "tmp": 21.9}}, "exg": {"src": "vB20", "val": {"NO2": {"cnc": 19.3}}}}
"""

from collections import OrderedDict

from scs_core.climate.sht_datum import SHTDatum

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.str import Str

from scs_core.gas.a4.a4_calibrated_datum import A4CalibratedDatum
from scs_core.gas.afe.afe_datum import AFEDatum
from scs_core.gas.afe.pt1000_datum import Pt1000Datum
from scs_core.gas.pid.pid_calibrated_datum import PIDCalibratedDatum
from scs_core.gas.scd30.scd30_datum import SCD30Datum

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class GasesSample(Sample):
    """
    classdocs
    """

    VERSION = 1.0

    __NON_ELECTROCHEM_FIELDS = ('pt1', 'sht', 'CO2', 'VOC', 'VOCe')
    __VOC_FIELDS = ('VOC', 'VOCe')

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

        src = jdict.get('src')
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
                sns[field] = A4CalibratedDatum.construct_from_jdict(node)

            if field in cls.__VOC_FIELDS:
                sns[field] = PIDCalibratedDatum.construct_from_jdict(node)

        electrochem_datum = AFEDatum(pt1000_datum, *list(sns.items()))

        return cls(tag, rec, scd30_datum, electrochem_datum, sht_datum, version=version, src=src, exegeses=exegeses)


    @classmethod
    def has_invalid_value(cls):
        # TODO: implement has_invalid_value
        return False


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, scd30_datum, electrochem_datum, sht_datum, version=None, src=None, exegeses=None):
        """
        Constructor
        """
        if version is None:
            version = self.VERSION

        super().__init__(tag, rec, version, src=src, exegeses=exegeses)

        self.__scd30_datum = scd30_datum                            # SCD30Datum
        self.__electrochem_datum = electrochem_datum                # AFEDatum or ISIDatum
        self.__sht_datum = sht_datum                                # SHT31Datum


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

        return "GasesSample:{tag:%s, rec:%s, src:%s, exegeses:%s, " \
               "scd30_datum:%s, electrochem_datum:%s, sht_datum:%s}" % \
            (self.tag, self.rec, self.src, exegeses,
             self.scd30_datum, self.electrochem_datum, self.sht_datum)
