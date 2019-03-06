#!/usr/bin/env python3

"""
Created on 27 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"rec": "2016-09-27T13:29:52.947+01:00", "val": {"opc_n2": {"pm1": 1, "pm2p5": 2, "pm10": 3, ' \
        '"per": 4, "bin1": {"1": 5, "2": 6}, "bin2": [[11, 22], {"key": {"inner": "value"}}], "mtf1": 9}}}'
print(jstr)
print("-")


# --------------------------------------------------------------------------------------------------------------------
# Construction...

jdict = json.loads(jstr)
print(jdict)
print("-")

datum = PathDict(jdict)
print(datum)
print("-")

jstr = JSONify.dumps(datum)
print(jstr)
print("-")

paths = datum.paths()
print(paths)
print("=")


# --------------------------------------------------------------------------------------------------------------------
# Accessing nodes...

path1 = "val.opc_n2.bin1"
print("path1: %s" % path1)

has_path = datum.has_path(path1)
print("has_path:%s" % has_path)

node = datum.node(path1)
print("node: %s" % node)
print("-")

path2 = "val.opc_n2.bin1.1"
print("path2: %s" % path2)

has_path = datum.has_path(path2)
print("has_path:%s" % has_path)

node = datum.node(path2)
print("node: %s" % node)
print("-")

path3 = "val.opc_n2.bin2"
print("path3: %s" % path3)

has_path = datum.has_path(path3)
print("has_path:%s" % has_path)

node = datum.node(path3)
print("node: %s" % node)
print("-")

path4 = "val.opc_n2.bin2:0:1"
print("path4: %s" % path4)

has_path = datum.has_path(path4)
print("has_path:%s" % has_path)

node = datum.node(path4)
print("node: %s" % node)
print("-")

path5 = "val.opc_n2.bin2:1.key.inner"
print("path5: %s" % path5)

has_path = datum.has_path(path5)
print("has_path:%s" % has_path)

node = datum.node(path5)
print("node: %s" % node)
print("=")


# --------------------------------------------------------------------------------------------------------------------
# Copying...

target = PathDict()
print("target: %s" % target)
print("-")

print("datum: %s" % datum)
jstr = JSONify.dumps(datum)
print(jstr)
print("-")

target.copy(datum, "rec")
print("target + rec: %s" % target)
jstr = JSONify.dumps(target)
print(jstr)
print("-")

target.copy(datum, "val.opc_n2.bin2:0:1")
print("target + val.opc_n2.bin2:0:1: %s" % target)
jstr = JSONify.dumps(target)
print(jstr)
print("=")

target = PathDict()
print("target: %s" % target)
print("-")

print("datum: %s" % datum)
jstr = JSONify.dumps(datum)
print(jstr)
print("-")

target.copy(datum, "val.opc_n2.bin2")
print("target + val.opc_n2.bin2: %s" % target)
jstr = JSONify.dumps(target)
print(jstr)
print("=")


# --------------------------------------------------------------------------------------------------------------------
# Appending...

target = PathDict()

print("datum: %s" % datum)
jstr = JSONify.dumps(datum)
print(jstr)
print("-")

source = "val.opc_n2.bin2:0"
print(source)
print("-")

target.copy(datum, source)
print(target)
jstr = JSONify.dumps(target)
print(jstr)
print("-")

source = "val.opc_n2.bin2:0:0"
print(source)
print("-")

target.copy(datum, source)
print(target)
jstr = JSONify.dumps(target)
print(jstr)
print("-")

new = "val.opc_n2.extra"
print(new)
print("-")

target.append(new, "hello")
print(target)
jstr = JSONify.dumps(target)
print(jstr)
print("-")

new = "val.opc_n2.bin2:0:1"
print(new)
print("-")

target.append(new, "bye")
print(target)
jstr = JSONify.dumps(target)
print(jstr)
print("-")
