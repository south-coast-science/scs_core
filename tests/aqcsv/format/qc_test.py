#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.format.qc import QC
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

QC.load()

print("list...")
for qc in QC.qcs():
    print(qc)
print("-")

print("find...")
code = "0"
qc = QC.find_by_code(code)
print("code:%s qc:%s" % (code, qc))
print(JSONify.dumps(qc))
print("-")

code = "a"
qc = QC.find_by_code(code)
print("code:%s unit:%s" % (code, qc))
print("-")

