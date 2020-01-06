#!/usr/bin/env python3

"""
Created on 6 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_core.gas.exegesis.sbl1.sbl1_no2_v1 import SBL1NO2v1
from scs_core.gas.exegesis.exegete_rendering_t_rh import ExegeteRenderingTRh


# --------------------------------------------------------------------------------------------------------------------
# run...

exegete = SBL1NO2v1.standard()
print(exegete)
print("-")

rendering = ExegeteRenderingTRh.construct(10, 90, 5, -10, 40, 5, exegete)

for row in rendering.rows():
    print(row)
print("-")

for row in rendering.rows():
    print(JSONify.dumps(row.as_json()))
print("-")

