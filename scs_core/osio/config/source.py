"""
Created on 19 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

 "SO2": {"weV": 0.294567, "aeV": 0.297067, "weC": -4.929433, "cnc": -14084.1}, "pt1": {"v": 0.325224, "tmp": 24.6},
 "sht": {"hmd": 60.9, "tmp": 25.9}}}

{"rec": "2017-03-04T12:07:22.627+00:00", "val": "CO": {"weV": 0.350568, "aeV": 0.275629, "weC": 0.052055, "cnc": 188.6},
"SO2": {"weV": 0.294379, "aeV": 0.296942, "weC": -4.929621, "cnc": -14084.6}, "pt1": {"v": 0.325208, "tmp": 24.5},
"sht": {"hmd": 60.9, "tmp": 25.9}}}
"""

from scs_core.osio.data.device import Device
from scs_core.osio.data.location import Location


# TODO: add device id message_tag to source

# TODO: we need to map AFE configs to device tags

# --------------------------------------------------------------------------------------------------------------------

class Source(object):
    """
    classdocs
    """

    DESCRIPTION =       "South Coast Science air quality monitoring device"

    TAGS = {28: ('no2', 'o3', 'no', 'co', 'pm1', 'pm2.5', 'pm10', 'temperature', 'humidity'),
            98: ('no2', 'o3', 'co', 'so2', 'pm1', 'pm2.5', 'pm10', 'temperature', 'humidity'),
            99: ('no2', 'co', 'so2', 'h2s', 'pm1', 'pm2.5', 'pm10', 'temperature', 'humidity')}


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def create(cls, device_id, api_auth, lat, lng, postcode, description):
        client_id = None
        name = device_id.box_label()
        desc = cls.DESCRIPTION if description is None else description
        password = None
        password_is_locked = None
        location = Location(lat, lng, None, None, postcode)
        device_type = device_id.type_label()
        batch = None
        org_id = api_auth.org_id
        owner_id = None
        tags = cls.TAGS[28]

        device = Device(client_id, name, desc, password, password_is_locked, location,
                        device_type, batch, org_id, owner_id, tags)

        return device


    @classmethod
    def update(cls, existing, lat, lng, postcode, description):
        client_id = None
        name = existing.name
        password = None
        password_is_locked = None
        device_type = existing.device_type
        batch = existing.batch
        org_id = None
        owner_id = None
        tags = existing.tags

        if lat and lng and postcode:
            location = Location(lat, lng, None, None, postcode)
        else:
            location = existing.location

        if description:
            desc = description
        else:
            desc = existing.description

        device = Device(client_id, name, desc, password, password_is_locked, location,
                        device_type, batch, org_id, owner_id, tags)

        return device
