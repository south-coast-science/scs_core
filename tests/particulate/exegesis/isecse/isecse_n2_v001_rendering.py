#!/usr/bin/env python3

"""
Created on 7 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_core.particulate.exegesis.exegete_rendering import ExegeteRendering
from scs_core.particulate.exegesis.isecse.isecse_n2_v002 import ISECSEN2v2


# --------------------------------------------------------------------------------------------------------------------
# run...

exegete = ISECSEN2v2.standard()
print(exegete)

rendering = ExegeteRendering.construct(10, 90, 5, exegete)

for row in rendering.rows():
    print("-")
    print(row)

print("=")

for row in rendering.rows():
    print(JSONify.dumps(row.as_json()))
