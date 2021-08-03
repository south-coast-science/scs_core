#!/usr/bin/env python3

"""
Created on 3 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.estate.package_version import PackageVersions

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

root = Host.scs_path()
# root = '/Users/bruno/Python/MacProject'


pvs1 = PackageVersions.construct_from_installation(root, Host)
print(pvs1)

jstr = JSONify.dumps(pvs1, indent=4)      # , indent=4
print(jstr)
print("-")

pvs2 = PackageVersions.construct_from_jdict(json.loads(jstr))
print(pvs2)

print(pvs2 == pvs1)
print("-")

version = pvs1.version('scs_core')
print(version)

version.save(Host)
