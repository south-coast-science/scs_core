"""
Created on 19 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.osio.data.device import Device


# --------------------------------------------------------------------------------------------------------------------

class ProjectClient(object):
    """
    classdocs
    """

    DEVICE_DESCRIPTION =       "South Coast Science air quality monitoring client"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def tags(cls):
        return ['SCS']


    @classmethod
    def create(cls, name, api_auth, description, tags):
        client_id = None
        desc = cls.DEVICE_DESCRIPTION if description is None else description
        password = None
        password_is_locked = None
        device_type = 'client'
        batch = None
        org_id = api_auth.org_id
        owner_id = None

        device = Device(client_id, name, desc, password, password_is_locked, None,
                        device_type, batch, org_id, owner_id, tags)

        return device


    @classmethod
    def update(cls, existing, description, tags=None):
        client_id = None
        name = existing.name
        password = None
        password_is_locked = None
        device_type = existing.device_type
        batch = existing.batch
        org_id = None
        owner_id = None

        device_tags = existing.tags if tags is None else tags

        if description:
            desc = description
        else:
            desc = existing.description

        device = Device(client_id, name, desc, password, password_is_locked, None,
                        device_type, batch, org_id, owner_id, device_tags)

        return device
