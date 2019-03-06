#!/usr/bin/env python3

"""
Created on 6 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import sys

from scs_core.aqcsv.data.aqcsv_record import AQCSVRecord


# --------------------------------------------------------------------------------------------------------------------

for line in sys.stdin:
    jstr = line.strip()

    record = AQCSVRecord.construct_from_jdict(json.loads(jstr))

    print(record)
    print("-")

    print(record.site())
    print("-")

    print(record.datetime())
    print("-")

    print(record.parameter())
    print("-")

    print(record.unit())
    print("-")

    print(record.qc())
    print("-")

    print(record.method())
    print("-")

    print(record.mpc())
    print("=")

    sys.stdout.flush()

