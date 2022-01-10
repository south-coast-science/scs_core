"""
Created on 26 Oct 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://medium.com/@houzier.saurav/aws-cognito-with-python-6a2867dd02c6

A class for storing and handling an organisation

"""


# --------------------------------------------------------------------------------------------------------------------

class Organisation(object):
    """
    classdocs
    """
    __TABLE_NAME = 'organisations'

    ORG_ID = 'OrganisationID'
    ORG_NAME = 'OrganisationName'
    ORG_OWNER = 'OrganisationOwner'
    ORG_ADMIN = 'OrganisationAdmin'
    ORG_URL = 'OrganisationURL'

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        id = jdict[cls.ORG_ID]
        name = jdict[cls.ORG_NAME]
        owner = jdict[cls.ORG_OWNER]
        url = jdict[cls.ORG_URL]

        return cls(id, name, owner, url)

    def __init__(self, id, name, owner, url):
        """
        Constructor
        """
        self._id = id  # int
        self._name = name  # string
        self._owner = owner  # string
        self._url = url  # string

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def owner(self):
        return self._owner

    @property
    def url(self):
        return self._url

    @owner.setter
    def owner(self, value):
        self._owner = value

    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Organisation:{id:%s, name:%s, admin:%s, url:%s}" % (self.id, self.name, self.owner, self.url)
