"""
Created on 19 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import numpy as np

from abc import ABC, abstractmethod
from collections import OrderedDict

from scs_core.data.json import JSONable


# TODO: check polynomial bounds values (see ErrorSurface)

# --------------------------------------------------------------------------------------------------------------------

class LinearEquation(JSONable, ABC):
    """
    classdocs
    """

    @staticmethod
    @abstractmethod                                 # bounds to be presented to CurveFit
    def default_coefficient_bounds():
        pass


    @classmethod
    def name(cls):
        return cls.__name__


    @classmethod
    def construct(cls, popt):                       # popt to be found from CurveFit
        # noinspection PyArgumentList
        return cls(*popt)


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def compute(self, x):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def display(self):
        pass


# --------------------------------------------------------------------------------------------------------------------

class LinE(LinearEquation):
    """
    classdocs
    """

    @staticmethod
    def func(x, ce, cex):
        return ce * np.exp(cex * x)


    @staticmethod
    def default_coefficient_bounds():
        lower = [0.0,  0.0]
        upper = [2.0,  1.0]

        return lower, upper


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ce, cex):
        self.__ce = ce
        self.__cex = cex


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, x):
        return self.func(x, self.__ce, self.__cex)


    def as_json(self):
        jdict = OrderedDict()

        jdict['ce'] = self.__ce
        jdict['cex'] = self.__cex

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def display(self):
        return "y ≈ %0.9f * exp(%0.9f * x)" % (self.__ce, self.__cex)


    def __str__(self, *args, **kwargs):
        return "LinE:{ce:%s, cex:%s}" %  (self.__ce, self.__cex)


# --------------------------------------------------------------------------------------------------------------------

class LinEC(LinearEquation):
    """
    classdocs
    """

    @staticmethod
    def func(x, ce, cex, c):
        return ce * np.exp(cex * x) + c


    @staticmethod
    def default_coefficient_bounds():
        lower = [0.0,  0.0, -1.0]
        upper = [2.0,  1.0,  2.0]

        return lower, upper


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ce, cex, c):
        self.__ce = ce
        self.__cex = cex
        self.__c = c


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, x):
        return self.func(x, self.__ce, self.__cex, self.__c)


    def as_json(self):
        jdict = OrderedDict()

        jdict['ce'] = self.__ce
        jdict['cex'] = self.__cex
        jdict['c'] = self.__c

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def display(self):
        return "y ≈ %0.9f * exp(%0.9f * x) + %0.9f" % (self.__ce, self.__cex, self.__c)


    def __str__(self, *args, **kwargs):
        return "LinEC:{ce:%s, cex:%s, c:%s}" %  (self.__ce, self.__cex, self.__c)


# --------------------------------------------------------------------------------------------------------------------

class LinEP1C(LinearEquation):
    """
    classdocs
    """

    @staticmethod
    def func(x, ce, cex, cx1, c):
        return ce * np.exp(cex * x) + cx1 * x + c


    @staticmethod
    def default_coefficient_bounds():
        lower = [0.0,  0.0, -0.1, -1.0]
        upper = [1.0,  1.0,  0.1,  1.0]

        return lower, upper


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ce, cex, cx1, c):
        self.__ce = ce
        self.__cex = cex
        self.__cx1 = cx1
        self.__c = c


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, x):
        return self.func(x, self.__ce, self.__cex, self.__cx1, self.__c)


    def as_json(self):
        jdict = OrderedDict()

        jdict['ce'] = self.__ce
        jdict['cex'] = self.__cex
        jdict['cx1'] = self.__cx1
        jdict['c'] = self.__c

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def display(self):
        return "y ≈ %0.9f * exp(%0.9f * x) + %0.9f * x + %0.9f" % (self.__ce, self.__cex, self.__cx1, self.__c)


    def __str__(self, *args, **kwargs):
        return "LinEP1C:{ce:%s, cex:%s, cx1:%s, c:%s}" %  (self.__ce, self.__cex, self.__cx1, self.__c)


# --------------------------------------------------------------------------------------------------------------------

class LinEP2C(LinearEquation):
    """
    classdocs
    """

    @staticmethod
    def func(x, ce, cex, cx2, cx1, c):
        return ce * np.exp(cex * x) + cx2 * x ** 2 + cx1 * x + c


    @staticmethod
    def default_coefficient_bounds():
        lower = [0.0,  0.0, -0.1, -0.1, -1.0]
        upper = [1.0,  1.0,  0.1,  0.1,  1.0]

        return lower, upper


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ce, cex, cx2, cx1, c):
        self.__ce = ce
        self.__cex = cex
        self.__cx2 = cx2
        self.__cx1 = cx1
        self.__c = c


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, x):
        return self.func(x, self.__ce, self.__cex, self.__cx2, self.__cx1, self.__c)


    def as_json(self):
        jdict = OrderedDict()

        jdict['ce'] = self.__ce
        jdict['cex'] = self.__cex
        jdict['cx2'] = self.__cx2
        jdict['cx1'] = self.__cx1
        jdict['c'] = self.__c

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def display(self):
        return "y ≈ %0.9f * exp(%0.9f * x) + %0.9f * x ^ 2 + %0.9f * x + %0.9f" % \
               (self.__ce, self.__cex, self.__cx2, self.__cx1, self.__c)


    def __str__(self, *args, **kwargs):
        return "LinEP2C:{ce:%s, cex:%s, cx2:%s, cx1:%s, c:%s}" %  \
               (self.__ce, self.__cex, self.__cx2, self.__cx1, self.__c)


# --------------------------------------------------------------------------------------------------------------------

class LinEP3C(LinearEquation):
    """
    classdocs
    """

    @staticmethod
    def func(x, ce, cex, cx3, cx2, cx1, c):
        return ce * np.exp(cex * x) + cx3 * x ** 3 + cx2 * x ** 2 + cx1 * x + c


    @staticmethod
    def default_coefficient_bounds():
        lower = [0.0,  0.0, -0.1, -0.1, -0.1, -1.0]
        upper = [0.1,  1.0,  0.1,  0.1,  0.1,  1.0]

        return lower, upper


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, ce, cex, cx3, cx2, cx1, c):
        self.__ce = ce
        self.__cex = cex
        self.__cx3 = cx3
        self.__cx2 = cx2
        self.__cx1 = cx1
        self.__c = c


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, x):
        return self.func(x, self.__ce, self.__cex, self.__cx3, self.__cx2, self.__cx1, self.__c)


    def as_json(self):
        jdict = OrderedDict()

        jdict['ce'] = self.__ce
        jdict['cex'] = self.__cex
        jdict['cx3'] = self.__cx3
        jdict['cx2'] = self.__cx2
        jdict['cx1'] = self.__cx1
        jdict['c'] = self.__c

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def display(self):
        return "y ≈ %0.9f * exp(%0.9f * x) + %0.9f * x ^ 3 + %0.9f * x ^ 2 + %0.9f * x + %0.9f" % \
               (self.__ce, self.__cex, self.__cx3, self.__cx2, self.__cx1, self.__c)


    def __str__(self, *args, **kwargs):
        return "LinEP3C:{ce:%s, cex:%s, cx3:%s, cx2:%s, cx1:%s, c:%s}" %  \
               (self.__ce, self.__cex, self.__cx3, self.__cx2, self.__cx1, self.__c)


# --------------------------------------------------------------------------------------------------------------------

class LinP1C(LinearEquation):
    """
    classdocs
    """

    @staticmethod
    def func(x, cx1, c):
        return cx1 * x + c


    @staticmethod
    def default_coefficient_bounds():
        lower = [-0.1, -1.0]
        upper = [0.1,  2.0]

        return lower, upper


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cx1, c):
        self.__cx1 = cx1
        self.__c = c


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, x):
        return self.func(x, self.__cx1, self.__c)


    def as_json(self):
        jdict = OrderedDict()

        jdict['cx1'] = self.__cx1
        jdict['c'] = self.__c

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def display(self):
        return "y ≈ %0.9f * x + %0.9f" % (self.__cx1, self.__c)


    def __str__(self, *args, **kwargs):
        return "LinP1C:{cx1:%s, c:%s}" %  (self.__cx1, self.__c)


# --------------------------------------------------------------------------------------------------------------------

class LinP2C(LinearEquation):
    """
    classdocs
    """

    @staticmethod
    def func(x, cx2, cx1, c):
        return cx2 * x ** 2 + cx1 * x + c


    @staticmethod
    def default_coefficient_bounds():
        lower = [-0.1, -0.1, -1.0]
        upper = [0.1,  0.1,  1.0]

        return lower, upper


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cx2, cx1, c):
        self.__cx2 = cx2
        self.__cx1 = cx1
        self.__c = c


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, x):
        return self.func(x, self.__cx2, self.__cx1, self.__c)


    def as_json(self):
        jdict = OrderedDict()

        jdict['cx2'] = self.__cx2
        jdict['cx1'] = self.__cx1
        jdict['c'] = self.__c

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def display(self):
        return "y ≈ %0.9f * x ^ 2 + %0.9f * x + %0.9f" % \
               (self.__cx2, self.__cx1, self.__c)


    def __str__(self, *args, **kwargs):
        return "LinP2C:{cx2:%s, cx1:%s, c:%s}" %  \
               (self.__cx2, self.__cx1, self.__c)


# --------------------------------------------------------------------------------------------------------------------

class LinP3C(LinearEquation):
    """
    classdocs
    """

    @staticmethod
    def func(x, cx3, cx2, cx1, c):
        return cx3 * x ** 3 + cx2 * x ** 2 + cx1 * x + c


    @staticmethod
    def default_coefficient_bounds():
        lower = [-0.1, -0.1, -0.1, -1.0]
        upper = [0.1,  0.1,  0.1,  1.0]

        return lower, upper


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cx3, cx2, cx1, c):
        self.__cx3 = cx3
        self.__cx2 = cx2
        self.__cx1 = cx1
        self.__c = c


    # ----------------------------------------------------------------------------------------------------------------

    def compute(self, x):
        return self.func(x, self.__cx3, self.__cx2, self.__cx1, self.__c)


    def as_json(self):
        jdict = OrderedDict()

        jdict['cx3'] = self.__cx3
        jdict['cx2'] = self.__cx2
        jdict['cx1'] = self.__cx1
        jdict['c'] = self.__c

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def display(self):
        return "y ≈ %0.9f * x ^ 3 + %0.9f * x ^ 2 + %0.9f * x + %0.9f" % \
               (self.__cx3, self.__cx2, self.__cx1, self.__c)


    def __str__(self, *args, **kwargs):
        return "LinP3C:{cx3:%s, cx2:%s, cx1:%s, c:%s}" %  \
               (self.__cx3, self.__cx2, self.__cx1, self.__c)
