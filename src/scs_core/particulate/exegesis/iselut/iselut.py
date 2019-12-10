"""
Created on 15 Nov 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

method: Immediate Scaling Error / Look-Up Table (ISELUT)
Brian Stacey's technique

domain: 0 <= rH <= max_rh
range: PM / error
"""

from abc import ABC
from collections import OrderedDict

from scs_core.data.json import JSONable, JSONify

from scs_core.particulate.exegesis.exegete import Exegete
from scs_core.particulate.exegesis.text import Text


# --------------------------------------------------------------------------------------------------------------------

class ISELUT(Exegete, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return cls.standard()

        rows = {}

        for row_jdict in jdict.get('rows'):
            row = ISELURow.construct_from_jdict(row_jdict)
            rows[row.rh_max] = row

        return cls(rows)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rows):
        """
        Constructor
        """
        super().__init__()

        self.__rows = rows                                  # dict of max_rh: ISELURow


    def __eq__(self, other):
        return self.__rows == other.__rows


    def __len__(self):
        return len(self.__rows)


    # ----------------------------------------------------------------------------------------------------------------

    def interpret(self, datum, rh):
        pm1 = self._interpret('pm1', datum.pm1, rh)
        pm2p5 = self._interpret('pm2p5', datum.pm2p5, rh)
        pm10 = self._interpret('pm10', datum.pm10, rh)

        return Text(pm1, pm2p5, pm10)


    # ----------------------------------------------------------------------------------------------------------------

    def _interpret(self, species, pm, rh):
        if pm is None or rh is None:
            return None

        row = self._row(rh)

        return pm * row.error(species, rh)


    def _row(self, rh):
        for max_rh, row in self.__rows.items():
            if rh <= max_rh:
                return row

        raise ValueError(rh)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        rows = []
        for row in self.__rows.values():
            rows.append(row.as_json())

        jdict['rows'] = rows

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        rows = '[' + ', '.join(JSONify.dumps(row) for row in self.__rows.values()) + ']'

        return self.__class__.__name__ + ":{rows:%s}" % rows


# --------------------------------------------------------------------------------------------------------------------

class ISELURow(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        rh_min = jdict.get('rh-min')
        rh_max = jdict.get('rh-max')

        scaling = jdict.get('scaling')

        return cls(rh_min, rh_max, scaling)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rh_min, rh_max, scaling):
        """
        Constructor
        """
        self.__rh_min = int(rh_min)
        self.__rh_max = int(rh_max)

        self.__scaling = scaling                     # dict of species: float


    def __eq__(self, other):
        return self.__rh_min == other.__rh_min and \
               self.__rh_max == other.__rh_max and \
               self.__scaling == other.__scaling


    # ----------------------------------------------------------------------------------------------------------------

    def error(self, species, _rh):
        scaling = self.__scaling[species]               # TODO: interpolate using rh?

        return scaling


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rh-min'] = self.__rh_min
        jdict['rh-max'] = self.__rh_max

        jdict['scaling'] = self.__scaling

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rh_max(self):
        return self.__rh_max


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ISELURow:{rh_min:%s, rh_max:%s, scaling:%s}" % (self.__rh_min, self.__rh_max, self.__scaling)
