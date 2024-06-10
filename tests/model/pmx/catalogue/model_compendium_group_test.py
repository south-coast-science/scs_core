#!/usr/bin/env python3

"""
Created on 7 June 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_core.model.pmx.catalogue.model_compendium import ModelCompendium
from scs_core.model.pmx.catalogue.model_compendium_group import ModelCompendiumGroup


# --------------------------------------------------------------------------------------------------------------------
# resources...

compendia = ModelCompendium.list()
print(compendia)
print("-")


# --------------------------------------------------------------------------------------------------------------------
# run...

c0 = ModelCompendium.retrieve(compendia[0])
print(c0)
print("-")

c1 = ModelCompendium.retrieve(compendia[1])
print(c1)
print("-")

group = ModelCompendiumGroup('OE.g1', {'NO2': c0, 'NO3': c1})
print(group)
print("-")

jstr = JSONify.dumps(group)
print(jstr)
print("-")

print(group.filename)
group.save(group.filename)
