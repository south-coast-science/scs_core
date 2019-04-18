"""
Created on 16 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

import scipy.stats as stats

from scs_core.data.error_sample import ErrorSample
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ErrorGridRhT(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, grid_rh_min, grid_rh_max, rh_step, grid_t_min, grid_t_max, t_step):
        cells = OrderedDict()

        # rH rows...
        rh_min = grid_rh_min
        rh_max = rh_min + rh_step

        while rh_min < grid_rh_max:
            cells[rh_max] = OrderedDict()

            # t cols...
            t_min = grid_t_min
            t_max = t_min + t_step

            while t_min < grid_t_max:
                cells[rh_max][t_max] = ErrorSample()

                t_min = t_max
                t_max += t_step

            rh_min = rh_max
            rh_max += rh_step

        # grid...
        return cls(grid_rh_min, grid_rh_max, rh_step, grid_t_min, grid_t_max, t_step, cells)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, grid_rh_min, grid_rh_max, rh_step, grid_t_min, grid_t_max, t_step, cells):
        """
        Constructor
        """
        self.__grid_rh_min = grid_rh_min            # float
        self.__grid_rh_max = grid_rh_max            # float
        self.__rh_step = rh_step                    # float

        self.__grid_t_min = grid_t_min              # float
        self.__grid_t_max = grid_t_max              # float
        self.__t_step = t_step                      # float

        self._cells = cells                         # OrderedDict of OrderedDict of ErrorSample


    def __len__(self):
        return len(self._cells)


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, rh, t, report, ref):
        # validate...
        if not self.grid_rh_min <= rh < self.grid_rh_max:
            return False

        if not self.grid_t_min <= t < self.grid_t_max:
            return False

        # find rH row...
        for rh_max in self._cells.keys():
            if rh < rh_max:
                # find t col...
                for t_max in self._cells[rh_max].keys():
                    if t < t_max:
                        self._cells[rh_max][t_max].append(report, ref)
                        return True

        return False


    def stdev(self):
        stdevs = []

        # rH rows...
        for row in self._cells.values():
            # t cols...
            for cell in row.values():
                stdev = cell.stdev()

                # append...
                if stdev is not None:
                    stdevs.append(stdev)

        # average...
        return round(sum(stdevs) / len(stdevs), 3)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        # t rows...
        t_min = self.grid_t_min
        t_max = t_min + self.t_step

        while t_min < self.grid_t_max:
            jdict = OrderedDict()

            # t cols...
            jdict['t_max'] = t_max
            jdict['t_avg'] = round((t_min + t_max) / 2, 1)

            # rH cols...
            rh_min = self.grid_rh_min
            rh_max = rh_min + self.rh_step

            while rh_min < self.grid_rh_max:
                cell = self._cells[rh_max][t_max]
                prefix = 'rH_' + str(rh_max)

                jdict[prefix + '_n'] = len(cell)
                jdict[prefix + '_stdev'] = cell.stdev()
                jdict[prefix + '_avg'] = cell.avg()

                rh_min = rh_max
                rh_max += self.rh_step

            yield jdict

            t_min = t_max
            t_max += self.t_step


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def grid_rh_min(self):
        return self.__grid_rh_min


    @property
    def grid_rh_max(self):
        return self.__grid_rh_max


    @property
    def rh_step(self):
        return self.__rh_step


    @property
    def grid_t_min(self):
        return self.__grid_t_min


    @property
    def grid_t_max(self):
        return self.__grid_t_max


    @property
    def t_step(self):
        return self.__t_step


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorGridRhT:{rh_min:%s, rh_max:%s, rh_step:%s, t_min:%s, t_max:%s, t_step:%s, rh deltas:%s}" % \
               (self.grid_rh_min, self.grid_rh_max, self.rh_step, self.grid_t_min, self.grid_t_max, self.t_step,
                len(self))


# --------------------------------------------------------------------------------------------------------------------

class ErrorGridTRh(ErrorGridRhT):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, grid_rh_min, grid_rh_max, rh_step, grid_t_min, grid_t_max, t_step, cells):
        """
        Constructor
        """
        super().__init__(grid_rh_min, grid_rh_max, rh_step, grid_t_min, grid_t_max, t_step, cells)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        # rH rows...
        rh_min = self.grid_rh_min
        rh_max = rh_min + self.rh_step

        while rh_min < self.grid_rh_max:
            jdict = OrderedDict()

            # rH cols...
            jdict['rH_max'] = rh_max
            jdict['rH_avg'] = round((rh_min + rh_max) / 2, 1)

            # t cols...
            t_min = self.grid_t_min
            t_max = t_min + self.t_step

            while t_min < self.grid_t_max:
                cell = self._cells[rh_max][t_max]
                prefix = 't_' + str(t_max)

                jdict[prefix + '_n'] = len(cell)
                jdict[prefix + '_stdev'] = cell.stdev()
                jdict[prefix + '_avg'] = cell.avg()

                t_min = t_max
                t_max += self.t_step

            yield jdict

            rh_min = rh_max
            rh_max += self.rh_step


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorGridTRh:{rh_min:%s, rh_max:%s, rh_step:%s, t_min:%s, t_max:%s, t_step:%s, t deltas:%s}" % \
               (self.grid_rh_min, self.grid_rh_max, self.rh_step, self.grid_t_min, self.grid_t_max, self.t_step,
                len(self))


# --------------------------------------------------------------------------------------------------------------------

class ErrorGridStats(ErrorGridRhT):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, grid_rh_min, grid_rh_max, rh_step, grid_t_min, grid_t_max, t_step, cells):
        """
        Constructor
        """
        super().__init__(grid_rh_min, grid_rh_max, rh_step, grid_t_min, grid_t_max, t_step, cells)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        # rH rows...
        rh_min = self.grid_rh_min
        rh_max = rh_min + self.rh_step

        while rh_min < self.grid_rh_max:
            count, col_t_min, col_t_max, means, samples = self.__t_stats(rh_max)

            # stats...
            mt, ct, r, p, std_err = stats.linregress(means, samples)

            jdict = OrderedDict()

            # rH cols...
            jdict['rH_max'] = rh_max
            jdict['rH_avg'] = round((rh_min + rh_max) / 2, 1)

            jdict['t_min'] = col_t_min
            jdict['t_max'] = col_t_max

            jdict['n'] = count

            jdict['mT'] = round(mt, 3)
            jdict['cT'] = round(ct, 3)
            jdict['r2'] = round(r ** 2, 3)

            yield jdict

            rh_min = rh_max
            rh_max += self.rh_step


    # ----------------------------------------------------------------------------------------------------------------

    def __t_stats(self, rh_max):
        count = 0
        col_t_min = None
        col_t_max = None

        means = []
        samples = []

        # t cols...
        t_min = self.grid_t_min
        t_max = t_min + self.t_step

        while t_min < self.grid_t_max:
            cell = self._cells[rh_max][t_max]

            if len(cell) > 0:
                means.append(round((t_min + t_max) / 2, 1))
                samples.append(cell.avg())

                if col_t_min is None:
                    col_t_min = t_min

                if col_t_max is None or t_max > col_t_max:
                    col_t_max = t_max

                count += len(cell)

            t_min = t_max
            t_max += self.t_step

        return count, col_t_min, col_t_max, means, samples


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorGridStats:{rh_min:%s, rh_max:%s, rh_step:%s, t_min:%s, t_max:%s, t_step:%s, t deltas:%s}" % \
               (self.grid_rh_min, self.grid_rh_max, self.rh_step, self.grid_t_min, self.grid_t_max, self.t_step,
                len(self))
