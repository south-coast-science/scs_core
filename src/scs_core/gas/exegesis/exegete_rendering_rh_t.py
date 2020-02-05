"""
Created on 6 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A CSV-friendly grid that can be used to visualise the error predicted by a given electrochem Exegete, using any T and
rH range or resolution.

This one has columns for rH and rows for T.
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.gas.exegesis.exegete import Exegete


# --------------------------------------------------------------------------------------------------------------------

class ExegeteRenderingRhT(JSONable):
    """
    classdocs
    """

    PRECISION = 1

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, gas, rh_min, rh_max, rh_delta, t_min, t_max, t_delta, exegete: Exegete):
        rows = [ExegeteRenderingRhTRow.construct(gas, rh_min, rh_max, rh_delta, t, exegete)
                for t in range(t_min, t_max + 1, t_delta)]

        return ExegeteRenderingRhT(rows)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rows):
        """
        Constructor
        """
        self.__rows = rows                          # array of ExegeteRenderingRhTRow


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        report = []

        for row in self.__rows:
            report.append(row.as_json())

        return report


    # ----------------------------------------------------------------------------------------------------------------

    def rows(self):
        for row in self.__rows:
            yield row


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        rows = '[' + ', '.join(str(row) for row in self.__rows) + ']'

        return "ExegeteRenderingRhT:{rows:%s}" % rows


# --------------------------------------------------------------------------------------------------------------------

class ExegeteRenderingRhTRow(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, gas, rh_min, rh_max, rh_delta, t, exegete: Exegete):
        cells = [ExegeteRenderingRhTCell(rh, exegete.error(gas, rh, t))
                 for rh in range(rh_min, rh_max + 1, rh_delta)]

        return ExegeteRenderingRhTRow(t, cells)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, t, cells):
        """
        Constructor
        """
        self.__t = t                                # float
        self.__cells = cells                        # array of ExegeteRenderingRhTCell


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['t'] = str(self.t) + ' °C'

        for cell in self.cells():
            jdict[cell.key()] = round(cell.error, ExegeteRenderingRhT.PRECISION)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def t(self):
        return self.__t


    def cells(self):
        for cell in self.__cells:
            yield cell


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        cells = '[' + ', '.join(str(cell) for cell in self.__cells) + ']'

        return "ExegeteRenderingRhTRow:{t:%s, cells:%s}" %  (self.t, cells)


# --------------------------------------------------------------------------------------------------------------------

class ExegeteRenderingRhTCell(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rh, error):
        """
        Constructor
        """
        self.__rh = rh                              # numeric
        self.__error = error                        # float


    # ----------------------------------------------------------------------------------------------------------------

    def key(self):
        return str(self.rh) + ' %'


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rh(self):
        return self.__rh


    @property
    def error(self):
        return self.__error


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ExegeteRenderingRhTCell:{rh:%s, error:%0.1f}" % (self.rh, self.error)
