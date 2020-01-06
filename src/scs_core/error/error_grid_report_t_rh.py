"""
Created on 20 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A CSV-friendly grid that can be used to analyse the errors collected by a given ErrorGrid.

This one has columns for T and rows for rH.
"""

from collections import OrderedDict

from scs_core.data.json import JSONable
from scs_core.error.error_grid import ErrorGrid


# --------------------------------------------------------------------------------------------------------------------

class ErrorGridReportTRh(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, grid: ErrorGrid):
        rows = []

        # rH rows...
        rh_min = grid.rh_min
        rh_max = rh_min + grid.rh_step

        while rh_min < grid.rh_max:
            # t cols...
            cells = []

            t_min = grid.t_min
            t_max = t_min + grid.t_step

            while t_min < grid.t_max:
                cell = grid.cells[rh_max][t_max]

                cells.append(ErrorGridReportTRhCell(t_max, len(cell), cell.stdev(), cell.avg()))

                t_min = t_max
                t_max += grid.t_step

            rows.append(ErrorGridReportTRhRow(rh_min, rh_max, cells))

            rh_min = rh_max
            rh_max += grid.rh_step

        return ErrorGridReportTRh(rows)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rows):
        """
        Constructor
        """
        self.__rows = rows                      # array of ErrorGridReportTRhRow


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

        return "ErrorGridReportTRh:{rows:%s}" % rows


# --------------------------------------------------------------------------------------------------------------------

class ErrorGridReportTRhRow(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rh_min, rh_max, cells):
        """
        Constructor
        """
        self.__rh_min = rh_min                  # float
        self.__rh_max = rh_max                  # float

        self.__cells = cells                    # array of ErrorGridReportTRhCell


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rh_max'] = self.rh_max
        jdict['rh_avg'] = round(self.rh_avg, 1)

        cells_jdict = OrderedDict()

        for cell in self.cells():
            cells_jdict[cell.key()] = cell.as_json()

        jdict['cells'] = cells_jdict

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rh_min(self):
        return self.__rh_min


    @property
    def rh_max(self):
        return self.__rh_max


    @property
    def rh_avg(self):
        return (self.__rh_min + self.__rh_max) / 2


    def cells(self):
        for cell in self.__cells:
            yield cell


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        cells = '[' + ', '.join(str(cell) for cell in self.__cells) + ']'

        return "ErrorGridReportTRhRow:{rh_min:%s, rh_max:%s, cells:%s}" %  (self.rh_min, self.rh_max, cells)


# --------------------------------------------------------------------------------------------------------------------

class ErrorGridReportTRhCell(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, t_max, n, stdev, avg):
        """
        Constructor
        """
        self.__t_max = t_max                    # float
        self.__n = n                            # int
        self.__stdev = stdev                    # float
        self.__avg = avg                        # float


    # ----------------------------------------------------------------------------------------------------------------

    def key(self):
        return 't_' + str(self.t_max)


    def as_json(self):
        jdict = OrderedDict()

        jdict['n'] = self.n
        jdict['stdev'] = self.stdev
        jdict['avg'] = self.avg

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def t_max(self):
        return self.__t_max


    @property
    def n(self):
        return self.__n


    @property
    def stdev(self):
        return self.__stdev


    @property
    def avg(self):
        return self.__avg


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorGridReportTRhCell:{t_max:%s, n:%s, stdev:%s, avg:%s}" % \
               (self.t_max, self.n, self.stdev, self.avg)
