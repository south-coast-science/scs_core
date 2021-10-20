"""
Created on 30 Sep 2021

@author: Jade Page (jade.page@southcoastscience.com)
https://medium.com/@houzier.saurav/aws-cognito-with-python-6a2867dd02c6

A single manager for all required cognito related functions.

Potential exceptions (for top level users?)
    except client.exceptions.NotAuthorizedException:
        return "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return "User is not confirmed"

"""
# --------------------------------------------------------------------------------------------------------------------

import base64
import hashlib
import hmac


# --------------------------------------------------------------------------------------------------------------------
import json


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
        )

        return res

    def delete_account(self, user):
        res = self.__cognito_client.admin_delete_user(
            UserPoolId=self.__pool_id,
            Username=user
        )

        return res

        # CognitoIdentityProvider.Client.exceptions.TooManyRequestsException
        # CognitoIdentityProvider.Client.exceptions.NotAuthorizedException
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

    # ----------------------------------------------------------------------------------------------------------------
    # User functionality
    # ----------------------------------------------------------------------------------------------------------------

    def password_change(self, token, old_pass, new_pass):
        res = self.__cognito_client.change_password(
            PreviousPassword=old_pass,
            ProposedPassword=new_pass,
            AccessToken=token
        )

        """
        CognitoIdentityProvider.Client.exceptions.ResourceNotFoundException
        CognitoIdentityProvider.Client.exceptions.InvalidParameterException
        CognitoIdentityProvider.Client.exceptions.InvalidPasswordException
        CognitoIdentityProvider.Client.exceptions.NotAuthorizedException
        CognitoIdentityProvider.Client.exceptions.TooManyRequestsException
        """


# --------------------------------------------------------------------------------------------------------------------

class CognitoCredentials(object):
    """
    classdocs
    """
    PASSWORD = 'password'
    ADMIN = 'is_admin'
    BODY_USER = 'user'
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
        username = data[cls.EVENT_USER]
        password = None
        email = data[cls.EVENT_EMAIL]

        return cls(username, password, email)

    def __init__(self, username, password, admin=False, email=None):
        """
        Constructor
        """
        self.__username = username  # string
        self.__password = password  # string
        self.__email = email  # string
        self.__admin = bool(admin)  # string > bool

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def admin(self):
        return self.__admin

    @property
    def email(self):
        return self.__email

    def __str__(self, *args, **kwargs):
        return "CognitoCredentials:{username:%s, password:%s, email:%s, admin:%s}" % self.username, \
               self.password, self.email, self.admin


# --------------------------------------------------------------------------------------------------------------------

class CognitoAccount(object):
    """
    classdocs
    """
    USER = "username"
    EMAIL = "email"
    FORENAME = "forename"
    SURNAME = "surname"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_qsp(cls, qsp):
        if not qsp:
            return None

        username = qsp.get(cls.USER)
        email = qsp.get(cls.EMAIL)
        forename = qsp.get(cls.FORENAME)
        surname = qsp.get(cls.SURNAME)

        return cls(username, email, forename, surname)

    def __init__(self, username, email, forename, surname, admin=False):
        """
        Constructor
        """
        self.__username = username  # string
        self.__forename = forename  # string
        self.__email = email  # string
        self.__admin = bool(admin)  # string > bool
        self.__surname = surname

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
    def email(self):
        return self.__email

    def __str__(self, *args, **kwargs):
        return "CognitoAccount:{username:%s, forename:%s, surname:%s, email:%s, admin:%s}" % self.username, \
               self.forename, self.surname, self.email, self.admin

