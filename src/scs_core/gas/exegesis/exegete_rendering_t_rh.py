"""
Created on 6 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A CSV-friendly grid that can be used to visualise the error predicted by a given electrochem Exegete, using any T and
rH range or resolution.

This one has columns for T and rows for rH (the more natural way of displaying temperature dependence as a
function of rH).
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.gas.exegesis.exegete import Exegete


# --------------------------------------------------------------------------------------------------------------------

class ExegeteRenderingTRh(JSONable):
    """
    classdocs
    """

    PRECISION = 1

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, gas, rh_min, rh_max, rh_delta, t_min, t_max, t_delta, exegete: Exegete):
        rows = [ExegeteRenderingTRhRow.construct(gas, rh, t_min, t_max, t_delta, exegete)
                for rh in range(rh_min, rh_max + 1, rh_delta)]

        return ExegeteRenderingTRh(rows)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rows):
        """
        Constructor
        """
        self.__rows = rows                              # array of ExegeteRenderingTRhRow


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

        return "ExegeteRenderingTRh:{rows:%s}" % rows


# --------------------------------------------------------------------------------------------------------------------

class ExegeteRenderingTRhRow(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, gas, rh, t_min, t_max, t_delta, exegete: Exegete):
        cells = [ExegeteRenderingTRhCell(t, exegete.error(gas, rh, t))
                 for t in range(t_min, t_max + 1, t_delta)]

        return ExegeteRenderingTRhRow(rh, cells)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rh, cells):
        """
        Constructor
        """
        self.__rh = rh                                  # numeric
        self.__cells = cells                            # array of ExegeteRenderingTRhCell


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rh'] = str(self.rh) + ' %'

        for cell in self.cells():
            jdict[cell.key()] = round(cell.error, ExegeteRenderingTRh.PRECISION)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rh(self):
        return self.__rh


    def cells(self):
        for cell in self.__cells:
            yield cell


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        cells = '[' + ', '.join(str(cell) for cell in self.__cells) + ']'

        return "ExegeteRenderingTRhRow:{rh:%s, cells:%s}" %  (self.rh, cells)


# --------------------------------------------------------------------------------------------------------------------

class ExegeteRenderingTRhCell(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, t, error):
        """
        Constructor
        """
        self.__t = t                                    # numeric
        self.__error = error                            # float


    # ----------------------------------------------------------------------------------------------------------------

    def key(self):
        return str(self.t) + ' °C'


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def t(self):
        return self.__t


    @property
    def error(self):
        return self.__error


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ExegeteRenderingTRhCell:{t:%s, error:%0.1f}" % (self.t, self.error)
