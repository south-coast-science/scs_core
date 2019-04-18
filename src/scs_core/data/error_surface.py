"""
Created on 18 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://joshualoong.com/2018/10/03/Fitting-Polynomial-Regressions-in-Python/
"""

import numpy as np
import scipy.stats as stats

from collections import OrderedDict

from scs_core.data.error_grid import ErrorGridStats
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

# noinspection PyTypeChecker
class ErrorSurface(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, grid_min_rh, grid_max_rh, rh_step, grid_min_t, grid_max_t, t_step):
        grid = ErrorGridStats.construct(grid_min_rh, grid_max_rh, rh_step, grid_min_t, grid_max_t, t_step)

        # grid...
        return cls(grid)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, grid):
        """
        Constructor
        """
        self.__grid = grid                      # ErrorGridStats


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, rh, t, report, ref):
        return self.__grid.append(rh, t, report, ref)


    def __compute_linear(self):
        rh_avgs = []
        mts = []
        cts = []

        # collect linear responses...
        for row in self.__grid.as_json():
            rh_avgs.append(row['rH_avg'])
            mts.append(row['mT'])
            cts.append(row['cT'])

        # compute surface...
        mt_mrh, mt_crh, mt_r, mt_p, mt_std_err = stats.linregress(rh_avgs, mts)
        ct_mrh, ct_crh, ct_r, ct_p, ct_std_err = stats.linregress(rh_avgs, cts)

        mt_weights = (mt_mrh, mt_crh)
        mt_r2 = mt_r ** 2

        ct_weights = (ct_mrh, ct_crh)
        ct_r2 = mt_r ** 2

        return mt_weights, mt_r2, ct_weights, ct_r2


    def __compute_poly(self):
        rh_avgs = []
        mts = []
        cts = []

        # collect linear responses...
        for row in self.__grid.as_json():
            rh_avgs.append(row['rH_avg'])
            mts.append(row['mT'])
            cts.append(row['cT'])

        x = np.array(rh_avgs)
        y = np.array(mts)

        mt_weights = np.polyfit(x, y, 2)

        y = np.array(cts)

        ct_weights = np.polyfit(x, y, 2)

        return mt_weights, None, ct_weights, None


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        # compute...
        mt_weights, mt_r2, ct_weights, ct_r2 = self.__compute_poly()

        # report...
        jdict = OrderedDict()

        jdict['mt_weights'] = [round(weight, 6) for weight in mt_weights]

        if mt_r2 is not None:
            jdict['mt_r2'] = round(mt_r2, 3)

        jdict['ct_weights'] = [round(weight, 6) for weight in ct_weights]

        if ct_r2 is not None:
            jdict['ct_r2'] = round(ct_r2, 3)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorSurface:{grid:%s}" % self.__grid
