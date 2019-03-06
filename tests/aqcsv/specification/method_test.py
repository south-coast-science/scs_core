#!/usr/bin/env python3

"""
Created on 6 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.aqcsv.specification.method import Method

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

for method in Method.instances():
    print(method)
print("-")

print("find by pk...")
pk = (42603, 31)
method = Method.instance(pk)
print("pk:%s method:%s" % (pk, method))
print("-")

jdict = method.as_json()
print(JSONify.dumps(method))
print("-")

print("remake...")
remade = Method.construct_from_jdict(jdict)
print(remade)
print("-")

print("equality...")
equality = remade == method
print("remade == method: %s" % equality)
print("-")

print("find by parameter_code...")
for method in Method.find_by_parameter_code(remade.parameter_code):
    print(method)
print("-")

print("find by method_code...")
for method in Method.find_by_method_code(remade.method_code):
    print(method)
print("-")
