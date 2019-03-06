#!/usr/bin/env python3

"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.mpc import MPC
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

print("list...")
for mpc in MPC.instances():
    print(mpc)
print("-")

print("find...")
code = 9
mpc = MPC.instance(code)
print("code:%s mpc:%s" % (code, mpc))
print("-")

code = 2
mpc = MPC.instance(code)
print("code:%s mpc:%s" % (code, mpc))

jdict = mpc.as_json()
print(JSONify.dumps(mpc))
print("-")

remade = MPC.construct_from_jdict(jdict)
print(remade)

equality = remade == mpc
print("remade == mpc: %s" % equality)
print("-")
