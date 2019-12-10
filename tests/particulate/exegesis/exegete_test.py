#!/usr/bin/env python3

"""
Created on 5 Dec 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.particulate.exegesis.exegete_catalogue import ExegeteCatalogue


# --------------------------------------------------------------------------------------------------------------------

names = ExegeteCatalogue.model_names()
print(names)
print("-")

model = ExegeteCatalogue.standard(names[0])
print(model)
