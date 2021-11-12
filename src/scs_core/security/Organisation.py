"""
Created on 26 Oct 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://medium.com/@houzier.saurav/aws-cognito-with-python-6a2867dd02c6

A class for storing and handling an organisation

"""
# --------------------------------------------------------------------------------------------------------------------

import json


# --------------------------------------------------------------------------------------------------------------------
import os


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


    @classmethod
    def construct_from_request(cls, body):
        if not body:
            return None

        jdict = json.loads(body)

        name = jdict[cls.ORG_NAME]
        owner = jdict[cls.ORG_OWNER]
        url = jdict[cls.ORG_URL]

        return cls(0, name, owner, url)

    @classmethod
    def retrieve_from_request(cls, body):
        if not body:
            return None

        jdict = json.loads(body)

        id = jdict[cls.ORG_ID]
        name = jdict[cls.ORG_NAME]
        owner = jdict[cls.ORG_OWNER]
        url = jdict[cls.ORG_URL]

        return cls(id, name, owner, url)


    def __init__(self, id, name, owner, url):
        """
        Constructor
        """
        self.__id = id  # int
        self.__name = name  # string
        self.__owner = owner  # string
        self.__url = url  # string

    def add_org(self):
        q = """INSERT INTO Organisations (OrganisationName, OrganisationOwner, OrganisationURL)
        VALUES('%s', '%s', '%s');""" % (self.__name, self.__owner, self.__url)

        return q

    def check_org_exists(self):
        q = """SELECT * FROM Organisations WHERE OrganisationName ='%s';""" % self.__name

        return q

    def construct_join_email(self, creds):
        filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'email_templates', 'request.txt')
        f = open(filepath, "r")
        message = f.read()

        message = (message.replace("USERNAME", creds.username))
        message = (message.replace("REQUESTEE_EMAIL", creds.email))
        message = (message.replace("ORGANISATION_NAME", self.name))

        return message

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def owner(self):
        return self.__owner

    @property
    def url(self):
        return self.__url

    @owner.setter
    def owner(self, value):
        self.__owner = value

    @staticmethod
    def create_table():
        q = """CREATE TABLE IF NOT EXISTS Organisations (
            OrganisationID int NOT NULL AUTO_INCREMENT,
            OrganisationName varchar(255) UNIQUE NOT NULL,
            OrganisationOwner varchar(255),
            OrganisationURL varchar(255),
            PRIMARY KEY (OrganisationID)
        );"""

        return q

    @staticmethod
    def drop_table():
        q = """DROP TABLE  Organisations;"""
        return q

    @staticmethod
    def create_org_admin_table():
        q = """CREATE TABLE IF NOT EXISTS OrgAdmins (
            OrganisationID int NOT NULL,
            OrganisationAdmin varchar(255)
        );"""

        return q


    @staticmethod
    def drop_org_admin_table():
        q = """DROP TABLE  OrgAdmins;"""
        return q

    @staticmethod
    def get_org_by_name(name):
        q = """SELECT * FROM Organisations WHERE OrganisationName ='%s';""" % name

        return q

    @staticmethod
    def get_org_owner(name):
        q = """SELECT OrganisationOwner FROM Organisations WHERE OrganisationName ='%s';""" % name

        return q

    @staticmethod
    def get_org_id_by_name(name):
        q = """SELECT OrganisationID FROM Organisations WHERE OrganisationName ='%s';""" % name

        return q

    @staticmethod
    def add_admin(admin_email, org_id):
        q = """INSERT INTO OrgAdmins (OrganisationID, OrganisationAdmin)
        VALUES('%s', '%s');""" % (org_id, admin_email)

        return q

    @staticmethod
    def remove_admin(admin_email, org_id):
        q = """DELETE FROM OrgAdmins WHERE OrganisationID = '%s' AND OrganisationAdmin = '%s';""" \
            % (org_id, admin_email)

        return q

    @staticmethod
    def get_org_admins_by_id(org_id):
        q = """SELECT OrganisationAdmin FROM OrgAdmins WHERE OrganisationId ='%s';""" % org_id

        return q


    @staticmethod
    def edit_url(new_url, org_id):
        q = """UPDATE Organisations SET OrganisationURL = '%s' WHERE OrganisationId ='%s';""" \
            % (new_url, org_id)
        return q

    @staticmethod
    def edit_owner(new_owner, org_id):
        q = """UPDATE Organisations SET OrganisationOwner = '%s' WHERE OrganisationId ='%s';""" \
            % (new_owner, org_id)
        return q
    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Organisation:{id:%s, name:%s, admin:%s, url:%s}" % (self.id, self.name, self.owner, self.url)
