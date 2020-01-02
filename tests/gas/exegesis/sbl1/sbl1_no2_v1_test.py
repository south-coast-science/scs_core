#!/usr/bin/env python3

"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.path_dict import PathDict

from scs_core.gas.exegesis.sbl1.sbl1_no2_v1 import SBL1NO2v1

# from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"val": {"NO2": {"weV": 0.3085, "cnc": 32.6, "aeV": 0.31, "weC": -0.0004}, ' \
       '"NO": {"weV": 0.27207, "cnc": -310.2, "aeV": 0.269, "weC": -0.00269}, ' \
       '"VOC": {"weC": 0.0971, "weV": 0.09388, "cnc": 1177.5}, ' \
       '"sht": {"hmd": 88.5, "tmp": 9.5}, "SO2": {"weV": 0.26507, "cnc": -47.6, "aeV": 0.26794, "weC": -0.00624}}, ' \
       '"rec": "2019-12-18T10:30:29Z", "tag": "scs-bgx-512"}'


# --------------------------------------------------------------------------------------------------------------------
# run...

exegete = SBL1NO2v1.standard()
print(exegete)
print("-")

# exegete.save(Host)
# exegete = SBL1NO2v1.load(Host)
# print(exegete)
# print("-")

datum = PathDict.construct_from_jstr(jstr)
print(datum)

text = datum.node('val.NO2.cnc')
print("text: %s" % text)
print("-")

for rh in range(10, 91, 5):
    for t in range(0, 46, 5):
        interpretation = exegete.interpret(text, t, rh)
        print("rh: %2d t: %2d text: %3.1f interpretation: %3.1f" % (rh, t, text, interpretation))

    print("-")
