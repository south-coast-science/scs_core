#!/usr/bin/env python3

"""
Created on 26 Oct 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify
from scs_core.data.path_dict import PathDict

from scs_core.particulate.exegesis.text import Text
from scs_core.particulate.exegesis.isecen2_v001 import ISECEN2v1

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

jstr = '{"val": {"mtf1": 13, "pm1": 7.7, "mtf5": 18, "pm2p5": 14.3, ' \
        '"bin": [266, 247, 189, 110, 50, 78, 41, 14, 4, 4, 1, 0, 0, 0, 0, 0], ' \
        '"mtf3": 16, "pm10": 25.1, "mtf7": 23, "per": 9.9}, ' \
        '"rec": "2019-10-26T11:27:38Z", "tag": "scs-bgx-401", "src": "N2"}'


# --------------------------------------------------------------------------------------------------------------------
# run...

exegete = ISECEN2v1.standard()
print(exegete)
print("-")

exegete.save(Host)
exegete = ISECEN2v1.load(Host)
print(exegete)
print("-")

path_name = 'exg.' + exegete.tag()

datum = PathDict.construct_from_jstr(jstr)

text = Text.construct_from_jdict(datum.node('val'))
print("text: %s" % text)
print("-")

for rh in range(0, 101, 5):
    interpretation = exegete.interpret(text, rh)
    datum.append(path_name, interpretation.as_json())
    print("rH:%s: %s" % (rh, JSONify.dumps(datum)))
