"""
Created on 11 Feb 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.datum import Datum
from scs_core.data.json import JSONable
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.gas.gas import Gas


# --------------------------------------------------------------------------------------------------------------------

class AirwatchRecord(JSONable):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_airwatch(cls, jdict, t, p):
        if jdict is None:
            return None

        if 'Date' not in jdict or 'Time' not in jdict:
            return None

        rec = LocalizedDatetime.construct_from_date_time(jdict.get('Date'), jdict.get('Time'))

        gases = []

        for key in jdict:
            if key != 'Date' and key != 'Time':
                gases.append(key)

        samples = {}

        for gas in gases:
            sample = AirwatchSample.construct_from_airwatch(gas, jdict.get(gas), t, p)

            if sample is not None:
                samples[gas] = sample

        # if not samples:
        #     return None

        return AirwatchRecord(rec, samples)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rec, samples):
        """
        Constructor
        """
        self.__rec = rec                                    # LocalizedDatetime
        self.__samples = samples                            # dict of name: AirwatchSample


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rec'] = self.rec.as_iso8601()
        jdict['val'] = self.samples

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec(self):
        return self.__rec


    @property
    def samples(self):
        return self.__samples


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        samples = '{' + ', '.join(gas + ': ' + str(sample) for gas, sample in self.samples.items()) + '}'

        return "AirwatchRecord:{rec:%s, samples:%s}" % (self.rec, samples)


# --------------------------------------------------------------------------------------------------------------------

class AirwatchSample(JSONable):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_airwatch(cls, gas, jdict, t, p):
        if jdict is None:
            return None

        status_units = jdict.get('Status')

        pieces = status_units.split(' ')

        if len(pieces) != 2:
            return None

        status = pieces[0]
        units = pieces[1]

        density = jdict.get('dns')

        try:
            float(density)
        except (TypeError, ValueError):
            return None

        concentration = Gas.concentration(gas, density, t, p)

        return AirwatchSample(status, units, density, concentration)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, units, density, concentration):
        """
        Constructor
        """
        self.__status = status                                      # string                    { P | R | A }
        self.__units = units                                        # string

        self.__density = Datum.float(density, 1)                    # float                     µg/m3
        self.__concentration = Datum.float(concentration, 1)        # float                     ppb


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['status'] = self.status
        jdict['units'] = self.units

        jdict['dns'] = self.density
        jdict['cnc'] = self.concentration

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def status(self):
        return self.__status


    @property
    def units(self):
        return self.__units


    @property
    def density(self):
        return self.__density


    @property
    def concentration(self):
        return self.__concentration


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AirwatchSample:{status:%s, units:%s, density:%s, concentration:%s}" % \
               (self.status, self.units, self.density, self.concentration)
