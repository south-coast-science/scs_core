#!/usr/bin/env python3

"""
Created on 17 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

data from: scs-bgx-431-ref-particulates-N2-climate-2019_15min_clipped_summary.numbers

https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
"""

import scipy.stats as stats

from scs_core.data.curve_fit import CurveFit
from scs_core.data.json import JSONify
from scs_core.data.linear_equation import LinE, LinEC, LinEP1C, LinEP2C, LinEP3C


# --------------------------------------------------------------------------------------------------------------------

rh =        (24.0, 27.5,  33.0,  37.7,  42.5,  47.6, 52.5,  57.5,  62.6,  67.4,  72.6,  77.4,  82.2,  86.5)

pm2p5 =     (1.050, 0.921, 1.197, 1.328, 1.519, 1.690, 1.725, 1.907, 2.182, 2.399, 2.992, 3.926, 4.802, 5.171)
pm10 =      (0.864, 0.778, 1.063, 1.161, 1.352, 1.487, 1.538, 1.697, 1.961, 2.179, 2.77, 3.656, 8.986, 20.532)

reported = pm10

print("pm10...")
print("==")


# --------------------------------------------------------------------------------------------------------------------

curve = CurveFit([])

for i in range(len(rh)):
    curve.append(rh[i], reported[i])

print(curve)
print("-")


# --------------------------------------------------------------------------------------------------------------------

for cls in LinE, LinEC, LinEP1C, LinEP2C, LinEP3C:
    popt, _ = curve.fit(cls.func, bounds=cls.default_coefficient_bounds())

    equation = cls.construct(popt)
    print(equation)
    print(equation.display())
    print(JSONify.dumps(equation.as_json()))
    print("-")

    synthesized = [round(equation.compute(x), 3) for x in rh]

    print("empirical: %s" % str(reported))
    print("synthetic: %s" % synthesized)
    print("-")

    slope, intercept, rvalue, pvalue, stderr = stats.linregress(reported, synthesized)
    r2 = rvalue ** 2

    print("r2: %0.6f" % r2)
    print("==")
