"""
Created on 26 Oct 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://medium.com/@houzier.saurav/aws-cognito-with-python-6a2867dd02c6

A class for storing and handling an organisation

"""
# --------------------------------------------------------------------------------------------------------------------

import json


# --------------------------------------------------------------------------------------------------------------------


class Organisation(object):
    """
    classdocs
    """
    __TABLE_NAME = 'organisations'

    ORG_ID = 'org_id'
    ORG_NAME = 'org_name'
    ORG_ADMIN = 'org_admin'
    ORG_URL = 'url'

    @classmethod
    def construct_from_request(cls, body):
        if not body:
            return None

        jdict = json.loads(body)

        name = jdict[cls.ORG_NAME]
        admin = jdict[cls.ORG_ADMIN]
        url = jdict[cls.ORG_URL]

        return cls(0, name, admin, url)


    def __init__(self, id, name, admin, url):
        """
        Constructor
        """
        self.__id = id  # int
        self.__name = name  # string
        self.__admin = admin  # string
        self.__url = url  # string

    def add_org(self):
        q = """INSERT INTO Organisations (OrganisationName, OrganisationAdmin, OrganisationURL)
        VALUES('%s', '%s', '%s');""" % (self.__name, self.__admin, self.__url)

        return q

    def check_org_exists(self):
        q = """SELECT * FROM Organisations WHERE OrganisationName ='%s';""" % self.__name

        return q


    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def admin(self):
        return self.__admin

    @property
    def url(self):
        return self.__url

    @admin.setter
    def admin(self, value):
        self.__admin = value

    @staticmethod
    def create_table():
        q = """CREATE TABLE IF NOT EXISTS Organisations (
            OrganisationID int NOT NULL AUTO_INCREMENT,
            OrganisationName varchar(255),
            OrganisationAdmin varchar(255),
            OrganisationURL varchar(255),
            PRIMARY KEY (OrganisationID)
        );"""

        return q

    @staticmethod
    def drop_table():
        q = """DROP TABLE  Organisations;"""
        return q

    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Organisation:{id:%s, name:%s, admin:%s, url:%s}" % (self.id, self.name, self.admin, self.url)
