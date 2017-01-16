'''
Created on 9 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

name: scs-rpi-006
client: 5392
pass: vXy5G44P

name: test
client: 5402
pass: cPhbitmp
'''

from collections import OrderedDict

from scs_core.common.json import JSONable
from scs_core.osio.data.location import Location


# --------------------------------------------------------------------------------------------------------------------

class Device(JSONable):
    '''
    classdocs
   '''

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def find_for_org(cls, http_client, api_key, org_id):
        pass


    @classmethod
    def find_for_user(cls, http_client, api_key, user_id):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        client_id = jdict.get('client-id')
        name = jdict.get('name')
        description = jdict.get('description')

        password = jdict.get('password')
        password_is_locked = jdict.get('password-is-locked')

        location = Location.construct_from_jdict(jdict.get('location'))

        device_type = jdict.get('device-type')
        batch = jdict.get('batch')

        org_id = jdict.get('org-id')
        owner_id = jdict.get('owner-id')

        tags = jdict.get('tags')

        return Device(client_id, name, description, password, password_is_locked, location, device_type, batch, org_id, owner_id, tags)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, client_id, name, description, password, password_is_locked, location, device_type, batch, org_id, owner_id, tags):
        '''
        Constructor
        '''
        self.__client_id = client_id                        # int
        self.__name = name                                  # string
        self.__description = description                    # string

        self.__password = password                          # string
        self.__password_is_locked = password_is_locked      # bool

        self.__location = location                          # Location

        self.__device_type = device_type                    # string
        self.__batch = batch                                # string

        self.__org_id = org_id                              # string
        self.__owner_id = owner_id                          # string

        self.__tags = tags                                  # array of string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        if self.client_id:
            jdict['client-id'] = self.client_id

        jdict['name'] = self.name
        jdict['description'] = self.description

        if self.password:
            jdict['password'] = self.password

        if self.password_is_locked:
            jdict['password-is-locked'] = self.password_is_locked

        jdict['location'] = self.location

        jdict['device-type'] = self.device_type
        jdict['batch'] = self.batch

        if self.org_id:
            jdict['org-id'] = self.org_id

        jdict['owner-id'] = self.owner_id

        jdict['tags'] = self.tags

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def client_id(self):
        return self.__client_id


    @property
    def name(self):
        return self.__name


    @property
    def description(self):
        return self.__description


    @property
    def password(self):
        return self.__password


    @property
    def password_is_locked(self):
        return self.__password_is_locked


    @property
    def location(self):
        return self.__location


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


    @property
    def tags(self):
        return self.__tags


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Device:{client_id:%s, name:%s, description:%s, password:%s, password_is_locked:%s, location:%s, device_type:%s, batch:%s, org_id:%s, owner_id:%s, tags:%s}" % \
                    (self.client_id, self.name, self.description, self.password, self.password_is_locked, self.location, self.device_type, self.batch, self.org_id, self.owner_id, self.tags)
