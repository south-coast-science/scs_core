#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.format.mpc import MPC
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

MPC.load()

print("list...")
for mcp in MPC.mcps():
    print(mcp)
print("-")

print("find...")
code = "2"
mcp = MPC.find_by_code(code)
print("code:%s mcp:%s" % (code, mcp))
print(JSONify.dumps(mcp))
print("-")

code = "9"
mcp = MPC.find_by_code(code)
print("code:%s unit:%s" % (code, mcp))
print("-")
