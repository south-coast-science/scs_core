#!/usr/bin/env python3

"""
Created on 5 Dec 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.particulate.exegesis.exegete import Exegete


# --------------------------------------------------------------------------------------------------------------------

names = Exegete.model_names()
print(names)
print("-")

model = Exegete.standard(names[0])
print(model)
