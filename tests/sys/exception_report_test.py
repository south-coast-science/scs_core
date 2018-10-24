#!/usr/bin/env python3

"""
Created on 9 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport


# --------------------------------------------------------------------------------------------------------------------
# run...

try:
    raise RuntimeError("test exception")

except Exception as ex:
    exr = ExceptionReport.construct(ex)
    print(exr)
    print("-")

    print(JSONify.dumps(exr), file=sys.stderr)

finally:
    print("done.")
