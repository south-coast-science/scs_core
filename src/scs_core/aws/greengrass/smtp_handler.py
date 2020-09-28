"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

https://blog.mailtrap.io/sending-emails-in-python-tutorial-with-code-examples/
"""

import smtplib
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
        try:
            with smtplib.SMTP(self.__smtp_server, self.__port) as server:
                server.login(self.__login, self.__password)
                server.sendmail(sender, receiver, message)
                print("Message sent")
        except (gaierror, ConnectionRefusedError):
            print('Failed to connect to SMTP Server (Refused) ')
        except smtplib.SMTPServerDisconnected:
            print('Failed to connect to SMTP Server (Disconnected) ')
        except smtplib.SMTPException as e:
            print('SMTP error occurred: ' + str(e))
