"""
Created on 16 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

An object providing a statistical report on sensor error, categorised by T and rH.
"""

from collections import OrderedDict

from scs_core.error.error_sample import ErrorSample


# --------------------------------------------------------------------------------------------------------------------

class ErrorGrid(object):
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

    def __init__(self, rh_min, rh_max, rh_step, t_min, t_max, t_step, cells):
        """
        Constructor
        """
        self.__rh_min = rh_min                      # float
        self.__rh_max = rh_max                      # float
        self.__rh_step = rh_step                    # float

        self.__t_min = t_min                        # float
        self.__t_max = t_max                        # float
        self.__t_step = t_step                      # float

        self.__cells = cells                        # OrderedDict of OrderedDict of ErrorSample


    def __len__(self):
        return len(self.__cells)


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, rh, t, report, ref):
        # validate...
        if not self.rh_min <= rh < self.rh_max:
            return False

        if not self.t_min <= t < self.t_max:
            return False

        # find rH row...
        for rh_max in self.__cells.keys():
            if rh < rh_max:
                # find T col...
                for t_max in self.__cells[rh_max].keys():
                    if t < t_max:
                        self.__cells[rh_max][t_max].append(report, ref)
                        return True

        return False


    def stdev(self):
        stdevs = []

        # rH rows...
        for row in self.__cells.values():
            # T cols...
            for cell in row.values():
                stdev = cell.stdev()

                # append...
                if stdev is not None:
                    stdevs.append(stdev)

        # average stdev...
        return round(sum(stdevs) / len(stdevs), 3)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rh_min(self):
        return self.__rh_min


    @property
    def rh_max(self):
        return self.__rh_max


    @property
    def rh_step(self):
        return self.__rh_step


    @property
    def t_min(self):
        return self.__t_min


    @property
    def t_max(self):
        return self.__t_max


    @property
    def t_step(self):
        return self.__t_step


    @property
    def cells(self):
        return self.__cells


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorGrid:{rh_min:%s, rh_max:%s, rh_step:%s, t_min:%s, t_max:%s, t_step:%s, rh deltas:%s}" % \
               (self.rh_min, self.rh_max, self.rh_step, self.t_min, self.t_max, self.t_step, len(self))
