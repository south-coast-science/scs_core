#!/usr/bin/env python3

"""
Created on 15 Nov 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_core.particulate.exegesis.text import Text
from scs_core.particulate.exegesis.iselut.iselut_n3_v001 import ISELUTN3v1

from scs_core.sample.sample import Sample

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"tag": "scs-bgx-512", "src": "N3", "rec": "2019-11-04T15:22:05Z", ' \
       '"val": {"per": 4.9, "pm1": 5.3, "pm2p5": 5.3, "pm10": 5.3, ' \
       '"bin": [85, 28, 18, 2, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ' \
       '"mtf1": 26, "mtf3": 30, "mtf5": 40, "mtf7": 0, "sfr": 4.54, "sht": {"hmd": 23.1, "tmp": 34.6}}}'


# --------------------------------------------------------------------------------------------------------------------
# run...

exegete = ISELUTN3v1.standard()
print(exegete)
print("-")

exegete.save(Host)
exegete = ISELUTN3v1.load(Host)
print(exegete)
print("-")

path_name = Sample.EXEGESIS_TAG + '.' + exegete.tag()

datum = PathDict.construct_from_jstr(jstr)

text = Text.construct_from_jdict(datum.node('val'))
print("text: %s" % text)
print("-")

for rh in range(0, 101, 5):
    interpretation = exegete.interpretation(text, rh)
    datum.append(path_name, interpretation.as_json())
    print("rH:%s: %s" % (rh, JSONify.dumps(datum)))
