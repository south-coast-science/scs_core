"""
Created on 18 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://joshualoong.com/2018/10/03/Fitting-Polynomial-Regressions-in-Python/
"""

import numpy as np
import scipy.stats as stats

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ErrorSurface(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, mesh):
        return cls.__compute_poly(mesh)


    @classmethod
    def __compute_linear(cls, mesh):
        rh_avgs = []
        mts = []
        cts = []

        # collect linear responses...
        for line in mesh.lines():
            rh_avgs.append(line.rh_avg)
            mts.append(line.m_t)
            cts.append(line.c_t)

        # compute surface...
        mt_mrh, mt_crh, mt_r, mt_p, mt_std_err = stats.linregress(rh_avgs, mts)
        ct_mrh, ct_crh, ct_r, ct_p, ct_std_err = stats.linregress(rh_avgs, cts)

        mt_weights = (mt_mrh, mt_crh)
        # mt_r2 = mt_r ** 2

        ct_weights = (ct_mrh, ct_crh)
        # ct_r2 = mt_r ** 2

        # return mt_weights, mt_r2, ct_weights, ct_r2
        return ErrorSurface(mt_weights, ct_weights)


    @classmethod
    def __compute_poly(cls, mesh):
        rh_avgs = []
        mts = []
        cts = []

        # collect linear responses...
        for line in mesh.lines():
            rh_avgs.append(line.rh_avg)
            mts.append(line.m_t)
            cts.append(line.c_t)

        # compute surface...
        x = np.array(rh_avgs)
        y = np.array(mts)

        mt_weights = np.polyfit(x, y, 2)

        y = np.array(cts)

        ct_weights = np.polyfit(x, y, 2)

        # TODO: add r2

        return ErrorSurface(mt_weights, ct_weights)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        mt_weights = jdict.get('mt_weights')
        ct_weights = jdict.get('ct_weights')

        return cls(mt_weights, ct_weights)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, mt_weights, ct_weights):
        """
        Constructor
        """
        self.__mt_weights = mt_weights                          # array of float
        self.__ct_weights = ct_weights                          # array of float

        self.__m_t_poly = np.poly1d(mt_weights)
        self.__c_t_poly = np.poly1d(ct_weights)


    def __eq__(self, other):
        return self.__mt_weights == other.__mt_weights and self.__ct_weights == other.__ct_weights


    # ----------------------------------------------------------------------------------------------------------------

    def error(self, rh, t):
        # numpy poly...
        m_t = self.__m_t_poly(rh)
        c_t = self.__c_t_poly(rh)

        # correction...
        error = (m_t * t) + c_t

        return error


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['mt_weights'] = [round(weight, 6) for weight in self.__mt_weights]
        # jdict['mt_r2'] = round(mt_r2, 3)

        jdict['ct_weights'] = [round(weight, 6) for weight in self.__ct_weights]
        # jdict['ct_r2'] = round(ct_r2, 3)

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mt_weight_b2(self):
        return self.__mt_weights[0]


    @property
    def mt_weight_b1(self):
        return self.__mt_weights[1]


    @property
    def mt_weight_b0(self):
        return self.__mt_weights[2]


    @property
    def ct_weight_b2(self):
        return self.__ct_weights[0]


    @property
    def ct_weight_b1(self):
        return self.__ct_weights[1]


    @property
    def ct_weight_b0(self):
        return self.__ct_weights[2]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ErrorSurface:{mt_weights:%s, ct_weights:%s}" %  (self.__mt_weights, self.__ct_weights)
