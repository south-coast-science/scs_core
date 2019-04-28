#!/usr/bin/env python3

"""
Created on 12 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.data.node_shifter import NodeShifter
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

d1 = PathDict({'1': 'a', '2': 'b', '3': 'c'})
print(JSONify.dumps(d1))

d2 = PathDict({'1': 'd', '2': 'e', '3': 'f'})
print(JSONify.dumps(d2))

d3 = PathDict({'1': 'g', '2': 'h', '3': 'i'})
print(JSONify.dumps(d3))

d4 = PathDict({'1': 'j', '2': 'k', '3': 'l'})
print(JSONify.dumps(d4))

print("-")


register = NodeShifter(2, True, '2')
print(register)

t0 = register.pop()
print(JSONify.dumps(t0))
print("-")

print("append...")
register.append(d1)
print(register)

print("pop...")
t1 = register.pop()
print(register)
print(JSONify.dumps(t1))
print("-")

print("append...")
register.append(d2)
print(register)

print("pop...")
t2 = register.pop()
print(register)
print(JSONify.dumps(t2))
print("-")

print("append...")
register.append(d3)
print(register)

print("pop...")
t3 = register.pop()
print(register)
print(JSONify.dumps(t3))
print("-")

print("append...")
register.append(d4)
print(register)

print("pop...")
t4 = register.pop()
print(register)
print(JSONify.dumps(t4))
print("=")

print("pop...")
t5 = register.pop()
print(register)
print(JSONify.dumps(t5))
print("-")

print("pop...")
t6 = register.pop()
print(register)
print(JSONify.dumps(t6))

print("pop...")
tx = register.pop()
print(register)
print(JSONify.dumps(tx))
print("=")

print(JSONify.dumps(t1))
print(JSONify.dumps(t2))
print(JSONify.dumps(t3))
print(JSONify.dumps(t4))
print(JSONify.dumps(t5))
print(JSONify.dumps(t6))
