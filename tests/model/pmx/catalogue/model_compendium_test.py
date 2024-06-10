#!/usr/bin/env python3

"""
Created on 7 June 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify

from scs_core.model.pmx.catalogue.model_compendium import ModelCompendium


# --------------------------------------------------------------------------------------------------------------------
# resources...

jstr = '{"data-set": "ref-scs-opc-116-gases-2021H1-vcal-slp-err", ' \
       '"period": {"start": "2021-02-10T10:15:00Z", "end": "2021-07-01T00:00:00Z"}, ' \
       '"primaries": {"NO2.vCal": {"path": "src.scs.env.gases.val.NO2.vCal", "min": -15.868, "avg": 9.993, ' \
       '"max": 66.966}}, ' \
       '"secondaries": {"tmp.brd": {"path": "src.scs.stat.val.tmp.brd", "min": 11.7, "avg": 24.912, "max": 42.8}, ' \
       '"hmd.cur": {"path": "src.scs.env.meteo.val.hmd.cur", "min": 18.7, "avg": 61.014, "max": 87.3}, ' \
       '"hmd.slope": {"path": "src.scs.env.meteo.val.hmd.slope", "min": -0.01, "avg": -0.0, "max": 0.014}, ' \
       '"tmp.cur": {"path": "src.scs.env.meteo.val.tmp.cur", "min": -1.4, "avg": 13.747, "max": 32.6}, ' \
       '"tmp.slope": {"path": "src.scs.env.meteo.val.tmp.slope", "min": -0.003, "avg": 0.0, "max": 0.002}}, ' \
       '"reference": {"path": "src.ref.NO2 (ppb)", "min": 0.5, "avg": 10.0, "max": 61.2}, ' \
       '"output": {"path": "exg.NO2.vE.OPCube.21H1", "min": 0.9, "avg": 10.0, "max": 53.8}, ' \
       '"performance": {"count": 13193, "slope": 0.886, "intercept": 1.141, "r2": 0.902, "p": 0.0, ' \
       '"std-err": 0.003}}'

# --------------------------------------------------------------------------------------------------------------------
# run...

compendia = ModelCompendium.list()
print(compendia)
print("-")

compendium = ModelCompendium.construct_from_jdict(json.loads(jstr))
print(compendium)
print("-")

name = compendium.name
print("name: %s" % name)
print("filename: %s" % compendium.filename)
print("vcal: %s" % compendium.primary_term('NO2.vCal').minimum)
print("-")

compendium.save(compendium.filename)
print("-")

summary = ModelCompendium.retrieve(name)
print(summary)
print("-")

print("name: %s" % summary.name)
print("species_name: %s" % summary.species_name)
print("model_name: %s" % summary.model_name)
print("device_name: %s" % summary.device_name)
print("period_name: %s" % summary.period_name)
print("-")
print("primary paths: %s" % summary.primary_paths())
print("secondary paths: %s" % summary.secondary_paths())
print("-")
print("is_error_prediction: %s" % summary.is_error_model)
print("=")

summary = ModelCompendium.retrieve('O3.vE.Urban.20H1')
print(summary)
print("-")

print("name: %s" % summary.name)
print("species_name: %s" % summary.species_name)
print("model_name: %s" % summary.model_name)
print("device_name: %s" % summary.device_name)
print("period_name: %s" % summary.period_name)
print("-")
print("primary paths: %s" % summary.primary_paths())
print("secondary paths: %s" % summary.secondary_paths())
print("-")
print("is_error_prediction: %s" % summary.is_error_model)
print("-")

print(JSONify.dumps(summary))
