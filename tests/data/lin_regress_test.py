#!/usr/bin/env python3

"""
Created on 18 Sep 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://www.w3schools.com/python/python_ml_linear_regression.asp
"""

import json

from scs_core.data.json import JSONify
from scs_core.data.lin_regress import LinRegress


# --------------------------------------------------------------------------------------------------------------------

x = [5, 7, 8, 7, 2, 17, 2, 9, 4, 11, 12, 9, 6]
y = [99, 86, 87, 88, 111, 86, 103, 87, 94, 78, 77, 85, 86]

regress = LinRegress.construct(x, y, prec=3)
print(len(regress))
print(regress)

jstr = JSONify.dumps(regress)
print(jstr)
print("-")

regress = LinRegress.construct_from_jdict(json.loads(jstr))
print(regress)
