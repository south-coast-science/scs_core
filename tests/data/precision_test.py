#!/usr/bin/env python3

"""
Created on 27 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.precision import Precision


# --------------------------------------------------------------------------------------------------------------------

precision = Precision()
print(precision)

precision.widen(0.123)
print(precision)

precision.widen(0.1234)
print(precision)

