"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
"""

import smtplib
import ssl
from socket import gaierror


# --------------------------------------------------------------------------------------------------------------------
class EmailHandler(object):
    def __init__(self, port, smtp_server, login, password):
        """
        Constructor
        """
        self.__port = port
        self.__smtp_server = smtp_server
        self.__login = login
        self.__password = password

    # ----------------------------------------------------------------------------------------------------------------
    def send_email(self, sender, receiver, message):
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL(self.__smtp_server, self.__port, context=context) as server:
                server.login(self.__login, self.__password)
                server.sendmail(sender, receiver, message)
        except (gaierror, ConnectionRefusedError):
            print('Failed to connect to SMTP Server (Refused) ')
        except smtplib.SMTPServerDisconnected:
            print('Failed to connect to SMTP Server (Disconnected) ')
        except smtplib.SMTPException as e:
            print('SMTP error occurred: ' + str(e))
