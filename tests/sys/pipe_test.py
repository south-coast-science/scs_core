#!/usr/bin/env python3

"""
Created on 30 Apr 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.subprocess import Pipe


# --------------------------------------------------------------------------------------------------------------------
# run...

pipe = Pipe(['echo', 'hello'],
            ['grep', 'hell'],
            ['grep', 'he'])

print(pipe)
print("-")

print(pipe.as_script())
print("-")

pipe.wait()
print("-")

output = pipe.check_output()
print(output)
print("-")

