"""
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example:
{
  "description": "BB development platform",
  "tags": [
    "pm1",
    "pm2.5",
    "pm10",
    "co",
    "no",
    "no2",
    "o3",
    "temperature",
    "humidity"
  ],
  "client-id": "5926",
  "name": "Alpha Pi Eng/V1 000006",
  "org-id": "south-coast-science-dev",
  "batch": null,
  "device-type": "Alpha Pi Eng/V1",
  "owner-id": "southcoastscience-dev",
  "location": {
    "lat": 50.819456,
    "lon": -0.128336,
    "postcode": "bn2 1af"
  }
}
"""

from scs_core.osio.data.device_summary import DeviceSummary
from scs_core.osio.data.location import Location


# --------------------------------------------------------------------------------------------------------------------

class Device(DeviceSummary):
    """
    classdocs
   """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        # DeviceSummary...
        client_id = jdict.get('client-id')
        name = jdict.get('name')
        description = jdict.get('description')

        location = Location.construct_from_jdict(jdict.get('location'))

        tags = jdict.get('tags')

        # Device...
        password = jdict.get('password')
        password_is_locked = jdict.get('password-is-locked')

        device_type = jdict.get('device-type')
        batch = jdict.get('batch')

        org_id = jdict.get('org-id')
        owner_id = jdict.get('owner-id')

        device = Device(client_id, name, description, password, password_is_locked, location,
                        device_type, batch, org_id, owner_id, tags)

        return device


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client_id, name, description, password, password_is_locked, location,
                 device_type, batch, org_id, owner_id, tags):
        """
        Constructor
        """
        DeviceSummary.__init__(self, client_id, name, description, location, tags)

        self.__password = password                          # string
        self.__password_is_locked = password_is_locked      # bool

        self.__device_type = device_type                    # string
        self.__batch = batch                                # string

        self.__org_id = org_id                              # string
        self.__owner_id = owner_id                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = DeviceSummary.as_json(self)

        if self.password is not None:
            jdict['password'] = self.password

        if self.password_is_locked is not None:
            jdict['password-is-locked'] = self.password_is_locked

        jdict['device-type'] = self.device_type

        if self.batch is not None:
            jdict['batch'] = self.batch

        if self.org_id is not None:
            jdict['org-id'] = self.org_id

        if self.owner_id is not None:
            jdict['owner-id'] = self.owner_id

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def password(self):
        return self.__password


    @property
    def password_is_locked(self):
        return self.__password_is_locked


    @property
    def device_type(self):
        return self.__device_type


    @property
    def batch(self):
        return self.__batch


    @property
    def org_id(self):
        return self.__org_id


    @property
    def owner_id(self):
        return self.__owner_id


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Device:{client_id:%s, name:%s, description:%s, password:%s, password_is_locked:%s, " \
               "location:%s, device_type:%s, batch:%s, org_id:%s, owner_id:%s, tags:%s}" % \
                    (self.client_id, self.name, self.description, self.password, self.password_is_locked,
                     self.location, self.device_type, self.batch, self.org_id, self.owner_id, self.tags)
