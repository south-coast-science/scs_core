#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.qc import QC
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

print("list...")
for qc in QC.instances():
    print(qc)
print("-")

print("find...")
code = 99
qc = QC.instance(code)
print("code:%s qc:%s" % (code, qc))
print("-")

code = 0
qc = QC.instance(code)
print("code:%s qc:%s" % (code, qc))

jdict = qc.as_json()
print(JSONify.dumps(qc))
print("-")

remade = QC.construct_from_jdict(jdict)
print(remade)

equality = remade == qc
print("remade == qc: %s" % equality)
print("-")
