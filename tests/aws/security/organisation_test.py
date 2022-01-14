#!/usr/bin/env python3

"""
Created on 14 Jan 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.aws.security.organisation import Organisation, OrganisationPathRoot, OrganisationUser, \
    OrganisationUserPath, OrganisationDevice

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------


organisation = Organisation(1, "Test Org", 'https://www.bbc.co.uk/news', "bruno.beloff@southcoastscience.com")
print(organisation)

jstr = JSONify.dumps(organisation)
print(jstr)

organisation = Organisation.construct_from_jdict(json.loads(jstr))
print(organisation)
print("-")

path_root = OrganisationPathRoot(11, 1, 'ricardo/')
print(path_root)

jstr = JSONify.dumps(path_root)
print(jstr)

path_root = OrganisationPathRoot.construct_from_jdict(json.loads(jstr))
print(path_root)
print("-")


user = OrganisationUser(111, 1, True, False)
print(user)

jstr = JSONify.dumps(user)
print(jstr)

user = OrganisationUser.construct_from_jdict(json.loads(jstr))
print(user)
print("-")

user_path = OrganisationUserPath(111, 11, 'heathrow/')
print(user_path)

jstr = JSONify.dumps(user_path)
print(jstr)

user_path = OrganisationUserPath.construct_from_jdict(json.loads(jstr))
print(user_path)
print("-")


device = OrganisationDevice('scs-bgx-401', 1, LocalizedDatetime.now(), None)
print(device)

jstr = JSONify.dumps(device)
print(jstr)

device = OrganisationDevice.construct_from_jdict(json.loads(jstr))
print(device)
print("-")

path = 'ric-ardo/'
print("is_valid_path: %s: %s" % (path, OrganisationPathRoot.is_valid_path(path)))

extension = 'x/a/'
print("is_valid_extension: %s: %s" % (extension, OrganisationUserPath.is_valid_extension(extension)))

device_tag = 'scs-be2-3'
print("is_valid_tag: %s: %s" % (device_tag, OrganisationDevice.is_valid_tag(device_tag)))

name = 'Dust Control Brazil (Demo)'
print("is_valid_name: %s: %s" % (name, Organisation.is_valid_name(name)))
