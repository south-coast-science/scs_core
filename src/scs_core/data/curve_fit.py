"""
Created on 17 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
https://www.answiz.com/questions/3958/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-polynomial-fitting?ref=anwser
"""

import numpy as np

import scipy.optimize as optimize


# TODO: check that the polynomial curve_fit matches the np.polyfit result (see ErrorSurface)

# --------------------------------------------------------------------------------------------------------------------

class CurveFit(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, points):
        """
        Constructor
        """
        self.__points = points


    def __len__(self):
        return len(self.__points)


    # ----------------------------------------------------------------------------------------------------------------

    def append(self, x, y):
        self.__points.append((x, y))


    def fit(self, func, bounds=(-np.inf, np.inf)):
        xdata = np.array(self.independents())
        ydata = np.array(self.dependents())

        popt, pcov = optimize.curve_fit(func, xdata, ydata, bounds=bounds)

        return popt, pcov


    # ----------------------------------------------------------------------------------------------------------------

    def independents(self):
        return [point[0] for point in self.__points]


    def dependents(self):
        return [point[1] for point in self.__points]


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CurveFit:{points:%s}" %  self.__points
