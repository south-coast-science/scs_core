"""
Created on 18 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import scipy.stats as stats

from collections import OrderedDict

from scs_core.data.error_grid import ErrorGridStats
from scs_core.data.json import JSONable


# TODO: needs polynomial fit mode

# --------------------------------------------------------------------------------------------------------------------

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

        self.__mt_mhr = None
        self.__mt_chr = None
        self.__mt_r2 = None

        self.__ct_mhr = None
        self.__ct_chr = None
        self.__ct_r2 = None



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
        self.__mt_mhr, self.__mt_chr, mt_r, mt_p, mt_std_err = stats.linregress(rh_avgs, mts)
        self.__ct_mhr, self.__ct_chr, ct_r, ct_p, ct_std_err = stats.linregress(rh_avgs, cts)

        self.__mt_r2 = mt_r ** 2
        self.__ct_r2 = ct_r ** 2


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        # compute...
        self.__compute_linear()

        # report...
        jdict = OrderedDict()

        jdict['mt_mhr'] = round(self.__mt_mhr, 3)
        jdict['mt_chr'] = round(self.__mt_chr, 3)
        jdict['mt_r2'] = round(self.__mt_r2, 3)

        jdict['ct_mhr'] = round(self.__ct_mhr, 3)
        jdict['ct_chr'] = round(self.__ct_chr, 3)
        jdict['ct_r2'] = round(self.__ct_r2, 3)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorSurface:{grid:%s}" % self.__grid
