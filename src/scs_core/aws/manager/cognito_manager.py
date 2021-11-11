"""
Created on 30 Sep 2021

@author: Jade Page (jade.page@southcoastscience.com)

https://medium.com/@houzier.saurav/aws-cognito-with-python-6a2867dd02c6

A single manager for all required cognito related functions.

"""
# --------------------------------------------------------------------------------------------------------------------
import ast
import base64
import hashlib
import hmac
import json

# --------------------------------------------------------------------------------------------------------------------
import logging


class CognitoManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cognito_client, app_id, app_id_secret, pool_id):
        self.__cognito_client = cognito_client
        self.__app_id = app_id
        self.__app_id_secret = app_id_secret
        self.__pool_id = pool_id

    # ----------------------------------------------------------------------------------------------------------------
    # Main functionality
    # ----------------------------------------------------------------------------------------------------------------

    def initiate_auth(self, user, password):
        hash_key = self.generate_hash(user)
        res = self.__cognito_client.admin_initiate_auth(
            UserPoolId=self.__pool_id,
            ClientId=self.__app_id,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': user,
                'SECRET_HASH': hash_key,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': user,
                'password': password,
            })

        return res

    def generate_hash(self, user):
        message = user + self.__app_id
        digest1 = hmac.new(str(self.__app_id_secret).encode('utf-8'),
                           msg=str(message).encode('utf-8'), digestmod=hashlib.sha256).digest()
        digest2 = base64.b64encode(digest1).decode()
        return digest2

    # ----------------------------------------------------------------------------------------------------------------
    # Admin functionality
    # ----------------------------------------------------------------------------------------------------------------

    def create_account(self, user, email, name, surname, admin=False):
        res = self.__cognito_client.admin_create_user(
            UserPoolId=self.__pool_id,
            Username=user,
            UserAttributes=[
                {"Name": "given_name", "Value": name},
                {"Name": "family_name", "Value": surname},
                {"Name": "email", "Value": email},
                {"Name": "custom:super", "Value": str(admin)},
            ],
            DesiredDeliveryMediums=[
                'EMAIL',
            ],
            MessageAction='SUPPRESS'
        )

        return res

    def set_password(self, user, password):
        res = self.__cognito_client.admin_set_user_password(
            UserPoolId=self.__pool_id,
            Username=user,
            Password=password,
            Permanent=True
        )

        return res

    def delete_account(self, user):
        res = self.__cognito_client.admin_delete_user(
            UserPoolId=self.__pool_id,
            Username=user
        )

        return res

        # CognitoIdentityProvider.Client.exceptions.UserNotFoundException

    def password_reset(self, user):
        res = self.__cognito_client.admin_reset_user_password(
            UserPoolId=self.__pool_id,
            Username=user
        )

        return res

    # CognitoIdentityProvider.Client.exceptions.TooManyRequestsException
    # CognitoIdentityProvider.Client.exceptions.NotAuthorizedException
    # CognitoIdentityProvider.Client.exceptions.UserNotFoundException

    def get_user_information(self, user):
        res = self.__cognito_client.admin_get_user(
            UserPoolId=self.__pool_id,
            Username=user
        )

        return res

    def make_super(self, user):
        res = self.__cognito_client.admin_update_user_attributes(
            UserPoolId=self.__pool_id,
            Username=user,
            UserAttributes=[
                {
                    'Name': 'custom:super',
                    'Value': 'True'
                }]
        )
        return res

    def is_super(self, user):
        b_is_admin = False
        x = self.get_user_information(user)
        for item in x["UserAttributes"]:
            if item["Name"] == "custom:super":
                b_is_admin = item["Value"]
                break

        return ast.literal_eval(b_is_admin)

    # ----------------------------------------------------------------------------------------------------------------
    # User functionality
    # ----------------------------------------------------------------------------------------------------------------

    def user_sign_up(self, user, password, name, surname, email, admin=False):
        res = self.__cognito_client.sign_up(
            ClientId=self.__app_id,
            SecretHash=self.generate_hash(user),
            Username=user,
            Password=password,
            UserAttributes=[
                {"Name": "given_name", "Value": name},
                {"Name": "family_name", "Value": surname},
                {"Name": "email", "Value": email},
                {"Name": "custom:super", "Value": str(admin)},
            ]
        )

        return res


    def password_change(self, token, old_pass, new_pass):
        res = self.__cognito_client.change_password(
            PreviousPassword=old_pass,
            ProposedPassword=new_pass,
            AccessToken=token
        )

        return res

    def admin_password_change(self, user, new_pass):
        res = self.__cognito_client.admin_set_user_password(
            UserPoolId=self.__pool_id,
            Username=user,
            Password=new_pass,
            Permanent=True
        )

        return res


# --------------------------------------------------------------------------------------------------------------------

class CognitoCredentials(object):
    """
    classdocs
    """
    PASSWORD = 'password'
    ADMIN = 'is_admin'
    BODY_USER = 'username'
    EVENT_USER = 'cognito:username'
    EVENT_EMAIL = 'email'

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_body(cls, body):
        if not body:
            return None

        jdict = json.loads(body)

        username = jdict[cls.BODY_USER]
        password = jdict[cls.PASSWORD]

        return cls(username, password)

    @classmethod
    def construct_from_event(cls, event):
        if not event:
            return None

        if not event["requestContext"]["authorizer"]["claims"]:
            return None

        data = event["requestContext"]["authorizer"]["claims"]
        logging.warning(data)
        username = data[cls.EVENT_USER]
        password = None
        email = data[cls.EVENT_EMAIL]

        return cls(username, password, False, email)

    def __init__(self, username, password, is_admin=False, email=None):
        """
        Constructor
        """
        self.__username = username  # string
        self.__password = password  # string
        self.__email = email  # string
        self.__is_admin = bool(is_admin)  # string > bool

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def is_admin(self):
        return self.__is_admin

    @property
    def email(self):
        return self.__email

    @is_admin.setter
    def is_admin(self, value):
        self.__is_admin = value

    def __str__(self, *args, **kwargs):
        return "CognitoCredentials:{username:%s, password:%s, email:%s, admin:%s}" % self.username, \
               self.password, self.email, self.is_admin


# --------------------------------------------------------------------------------------------------------------------

class CognitoAccount(object):
    """
    classdocs
    """
    USER = "username"
    EMAIL = "email"
    FORENAME = "forename"
    SURNAME = "surname"
    PASSWORD = "password"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_body(cls, body):
        if not body:
            return None

        jdict = json.loads(body)

        username = jdict[cls.USER]
        password = jdict[cls.PASSWORD]
        email = jdict[cls.EMAIL]
        forename = jdict[cls.FORENAME]
        surname = jdict[cls.SURNAME]


        return cls(username, email, forename, surname, password)

    def __init__(self, username, email, forename, surname, password, admin=False):
        """
        Constructor
        """
        self.__username = username  # string
        self.__forename = forename  # string
        self.__email = email  # string
        self.__admin = bool(admin)  # string > bool
        self.__surname = surname
        self.__password = password

    @property
    def username(self):
        return self.__username

    @property
    def forename(self):
        return self.__forename

    @property
    def surname(self):
        return self.__surname

    @property
    def admin(self):
        return self.__admin

    @property
    def password(self):
        return self.__password

    @property
    def email(self):
        return self.__email

    def __str__(self, *args, **kwargs):
        return "CognitoAccount:{username:%s, forename:%s, surname:%s, email:%s, admin:%s}" % self.username, \
               self.forename, self.surname, self.email, self.admin

