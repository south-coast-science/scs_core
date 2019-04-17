"""
Created on 16 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.error_sample import ErrorSample
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ErrorGridRhT(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, grid_min_rh, grid_max_rh, rh_step, grid_min_t, grid_max_t, t_step):
        cells = OrderedDict()

        # rH rows...
        min_rh = grid_min_rh
        max_rh = min_rh + rh_step

        while min_rh < grid_max_rh:
            cells[max_rh] = OrderedDict()

            # t cols...
            min_t = grid_min_t
            max_t = min_t + t_step

            while min_t < grid_max_t:
                cells[max_rh][max_t] = ErrorSample()

                min_t = max_t
                max_t += t_step

            min_rh = max_rh
            max_rh += rh_step

        # grid...
        return cls(grid_min_rh, grid_max_rh, rh_step, grid_min_t, grid_max_t, t_step, cells)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, grid_min_rh, grid_max_rh, rh_step, grid_min_t, grid_max_t, t_step, cells):
        """
        Constructor
        """
        self.__grid_min_rh = grid_min_rh            # float
        self.__grid_max_rh = grid_max_rh            # float
        self.__rh_step = rh_step                    # float

        self.__grid_min_t = grid_min_t              # float
        self.__grid_max_t = grid_max_t              # float
        self.__t_step = t_step                      # float

        self._cells = cells                         # OrderedDict of OrderedDict of ErrorSample


    def __len__(self):
        return len(self._cells)


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, rh, t, report, ref):
        # validate...
        if not self.grid_min_rh <= rh < self.grid_max_rh:
            return False

        if not self.grid_min_t <= t < self.grid_max_t:
            return False

        # find rH row...
        for max_rh in self._cells.keys():
            if rh < max_rh:
                # find t col...
                for max_t in self._cells[max_rh].keys():
                    if t < max_t:
                        self._cells[max_rh][max_t].append(report, ref)
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
        min_t = self.grid_min_t
        max_t = min_t + self.t_step

        while min_t < self.grid_max_t:
            jdict = OrderedDict()

            # t cols...
            jdict['t_max'] = max_t
            jdict['t_avg'] = round((min_t + max_t) / 2, 1)

            # rH cols...
            min_rh = self.grid_min_rh
            max_rh = min_rh + self.rh_step

            while min_rh < self.grid_max_rh:
                cell = self._cells[max_rh][max_t]
                prefix = 'rh_' + str(max_rh)

                jdict[prefix + '_n'] = len(cell)
                jdict[prefix + '_stdev'] = cell.stdev()
                jdict[prefix + '_avg'] = cell.avg()

                min_rh = max_rh
                max_rh += self.rh_step

            yield jdict

            min_t = max_t
            max_t += self.t_step


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def grid_min_rh(self):
        return self.__grid_min_rh


    @property
    def grid_max_rh(self):
        return self.__grid_max_rh


    @property
    def rh_step(self):
        return self.__rh_step


    @property
    def grid_min_t(self):
        return self.__grid_min_t


    @property
    def grid_max_t(self):
        return self.__grid_max_t


    @property
    def t_step(self):
        return self.__t_step


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorGridRhT:{min_rh:%s, max_rh:%s, rh_step:%s, min_t:%s, max_t:%s, t_step:%s, rh deltas:%s}" % \
               (self.grid_min_rh, self.grid_max_rh, self.rh_step, self.grid_min_t, self.grid_max_t, self.t_step,
                len(self))


# --------------------------------------------------------------------------------------------------------------------

class ErrorGridTRh(ErrorGridRhT):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, grid_min_rh, grid_max_rh, rh_step, grid_min_t, grid_max_t, t_step, cells):
        """
        Constructor
        """
        super().__init__(grid_min_rh, grid_max_rh, rh_step, grid_min_t, grid_max_t, t_step, cells)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        # rH rows...
        min_rh = self.grid_min_rh
        max_rh = min_rh + self.rh_step

        while min_rh < self.grid_max_rh:
            jdict = OrderedDict()

            # rH cols...
            jdict['rh_max'] = max_rh
            jdict['rh_avg'] = round((min_rh + max_rh) / 2, 1)

            # t cols...
            min_t = self.grid_min_t
            max_t = min_t + self.t_step

            while min_t < self.grid_max_t:
                cell = self._cells[max_rh][max_t]
                prefix = 't_' + str(max_t)

                jdict[prefix + '_n'] = len(cell)
                jdict[prefix + '_stdev'] = cell.stdev()
                jdict[prefix + '_avg'] = cell.avg()

                min_t = max_t
                max_t += self.t_step

            yield jdict

            min_rh = max_rh
            max_rh += self.rh_step


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorGridTRh:{min_rh:%s, max_rh:%s, rh_step:%s, min_t:%s, max_t:%s, t_step:%s, t deltas:%s}" % \
               (self.grid_min_rh, self.grid_max_rh, self.rh_step, self.grid_min_t, self.grid_max_t, self.t_step,
                len(self))
