"""
Created on 24 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.gas.pid.pid import PID
from scs_core.gas.pid.pid_temp_comp import PIDTempComp


# --------------------------------------------------------------------------------------------------------------------

PIDTempComp.init()      # must be initialised before sensors
PID.init()
