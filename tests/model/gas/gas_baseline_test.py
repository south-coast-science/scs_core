#!/usr/bin/env python3

"""
Created on 19 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.gas.sensor_baseline import BaselineEnvironment, SensorBaseline
from scs_core.model.gas.gas_baseline import GasBaseline


# --------------------------------------------------------------------------------------------------------------------

environment = BaselineEnvironment('41.5', '22.1', None)
print(environment)

# baseline1 = SensorBaseline()
