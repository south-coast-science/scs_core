"""
Created on 19 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.osio.data.device import Device
from scs_core.osio.data.location import Location


# TODO: we need to map AFE configs to device tags

# --------------------------------------------------------------------------------------------------------------------

class Source(object):
    """
    classdocs
    """

    DESCRIPTION =       "South Coast Science air quality monitoring device."
    TAGS =              ('pm1', 'pm2.5', 'pm10', 'co', 'no', 'no2', 'o3', 'temperature', 'humidity')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def device(cls, device_id, client_auth, api_auth, lat, lng, postcode):
        client_id = None
        name = device_id.box_label()
        description = cls.DESCRIPTION
        password = None
        password_is_locked = False
        location = Location(lat, lng, None, None, postcode)
        device_type = device_id.type_label()
        batch = None
        org_id = api_auth.org_id
        owner_id = client_auth.client_id
        tags = cls.TAGS

        device = Device(client_id, name, description, password, password_is_locked, location,
                        device_type, batch, org_id, owner_id, tags)

        return device


    @classmethod
    def command(cls):
        pass
