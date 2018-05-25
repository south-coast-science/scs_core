"""
Created on 19 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.osio.config.project_topic import ProjectTopic
from scs_core.osio.data.device import Device
from scs_core.osio.data.location import Location


# --------------------------------------------------------------------------------------------------------------------

class ProjectSource(object):
    """
    classdocs
    """

    DEVICE_DESCRIPTION =       "South Coast Science air quality monitoring device"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def tags(cls, afe_calib, include_particulates):
        gases_topic = ProjectTopic.get_gases_topic(afe_calib.gas_names())

        # TODO: check for CO2 / NDIR topic

        tags = ['SCS']

        if gases_topic:
            tags.extend(gases_topic.tags)

        if include_particulates:
            tags.extend(ProjectTopic.PARTICULATES.tags)

        tags.extend(ProjectTopic.CLIMATE.tags)

        return tags


    @classmethod
    def create(cls, system_id, api_auth, lat, lng, postcode, description, tags):
        client_id = None
        name = system_id.box_label()
        desc = cls.DEVICE_DESCRIPTION if description is None else description
        password = None
        password_is_locked = None
        location = Location(lat, lng, None, None, postcode)
        device_type = system_id.type_label()
        batch = None
        org_id = api_auth.org_id
        owner_id = None

        device = Device(client_id, name, desc, password, password_is_locked, location,
                        device_type, batch, org_id, owner_id, tags)

        return device


    @classmethod
    def update(cls, existing, lat, lng, postcode, description, tags=None):
        client_id = None
        name = existing.name
        password = None
        password_is_locked = None
        device_type = existing.device_type
        batch = existing.batch
        org_id = None
        owner_id = None

        device_tags = existing.tags if tags is None else tags

        if lat and lng and postcode:
            location = Location(lat, lng, None, None, postcode)
        else:
            location = existing.location

        if description:
            desc = description
        else:
            desc = existing.description

        device = Device(client_id, name, desc, password, password_is_locked, location,
                        device_type, batch, org_id, owner_id, device_tags)

        return device
