"""
Created on 24 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alphasense A4 electrochemical sensors
"""

from scs_core.gas.a4.a4 import A4
from scs_core.gas.a4.a4_temp_comp import A4TempComp


# --------------------------------------------------------------------------------------------------------------------

A4TempComp.init()       # must be initialised before sensors
A4.init()
