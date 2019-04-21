"""
Created on 20 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import scipy.stats as stats

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ErrorGridMeshTRh(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, grid):
        lines = []

        # rH lines...
        rh_min = grid.rh_min
        rh_max = rh_min + grid.rh_step

        while rh_min < grid.rh_max:
            n, col_t_min, col_t_max, means, samples = cls.__t_stats(grid, rh_max)

            if len(means) > 1 and len(samples) > 1:
                # stats...
                m_t, c_t, r, p, std_err = stats.linregress(means, samples)

                lines.append(ErrorGridMeshTRhLine(rh_min, rh_max, col_t_min, col_t_max, n, m_t, c_t, r ** 2))

            rh_min = rh_max
            rh_max += grid.rh_step

        return ErrorGridMeshTRh(lines)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __t_stats(cls, grid, rh_max):
        count = 0
        col_t_min = None
        col_t_max = None

        means = []
        samples = []

        # t cols...
        t_min = grid.t_min
        t_max = t_min + grid.t_step

        while t_min < grid.t_max:
            cell = grid.cells[rh_max][t_max]

            if len(cell) > 0:
                means.append(round((t_min + t_max) / 2, 1))
                samples.append(cell.avg())

                if col_t_min is None:
                    col_t_min = t_min

                if col_t_max is None or t_max > col_t_max:
                    col_t_max = t_max

                count += len(cell)

            t_min = t_max
            t_max += grid.t_step

        return count, col_t_min, col_t_max, means, samples


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, lines):
        """
        Constructor
        """
        self.__lines = lines


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        report = []

        for line in self.__lines:
            report.append(line.as_json())

        return report


    # ----------------------------------------------------------------------------------------------------------------

    def lines(self):
        for line in self.__lines:
            yield line


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        lines = '[' + ', '.join(str(line) for line in self.__lines) + ']'

        return "ErrorGridMeshTRh:{lines:%s}" % lines


# --------------------------------------------------------------------------------------------------------------------

class ErrorGridMeshTRhLine(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, rh_min, rh_max, t_min, t_max, n, m_t, c_t, r2):
        """
        Constructor
        """
        self.__rh_min = rh_min                  # float
        self.__rh_max = rh_max                  # float

        self.__t_min = t_min                    # float
        self.__t_max = t_max                    # float

        self.__n = n                            # int

        self.__m_t = m_t                        # float
        self.__c_t = c_t                        # float
        self.__r2 = r2                          # float


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['rH_max'] = self.rh_max
        jdict['rH_avg'] = round(self.rh_avg, 1)

        jdict['t_min'] = self.t_min
        jdict['t_max'] = self.t_max

        jdict['n'] = self.n

        jdict['mT'] = round(self.m_t, 3)
        jdict['cT'] = round(self.c_t, 3)
        jdict['r2'] = round(self.r2, 3)

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


    @property
    def t_min(self):
        return self.__t_min


    @property
    def t_max(self):
        return self.__t_max


    @property
    def n(self):
        return self.__n


    @property
    def m_t(self):
        return self.__m_t


    @property
    def c_t(self):
        return self.__c_t


    @property
    def r2(self):
        return self.__r2


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorGridMeshTRhLine:{rh_min:%s, rh_max:%s, t_min:%s, t_max:%s, n:%s, m_t:%s, c_t:%s, r2:%s}" % \
               (self.rh_min, self.rh_max, self.t_min, self.t_max, self.n, self.m_t, self.c_t, self.r2)
