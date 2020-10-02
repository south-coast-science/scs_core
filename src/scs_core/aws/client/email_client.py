"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
"""
import smtplib
import ssl
from socket import gaierror


# --------------------------------------------------------------------------------------------------------------------
class EmailClient(object):

    __PORT = 465
    __SMTP_SERVER = "smtp.gmail.com"
    __EMAIL_ADDRESS = "devicetest147147@gmail.com"
    __EMAIL_PASSWORD = "Southern!"

    # Change from private class vars to conf eventually ?

    def __init__(self, port=0, smtp_server="", login_address="", password=""):
        """
        Constructor
        """
        self.__port = port
        self.__smtp_server = smtp_server
        self.__sender_email = login_address
        self.__password = password

    # ----------------------------------------------------------------------------------------------------------------
    def send_email(self, receiver, message):
        context = ssl.create_default_context()
        message = 'Subject: {}\n\n{}'.format("SCS Device Status", message)
        if not self.__port or not self.__smtp_server or not self.__sender_email or not self.__password:
            return "Email Client Not Configured"
        try:
            with smtplib.SMTP_SSL(self.__smtp_server, self.__port, context=context) as server:
                server.login(self.__sender_email, self.__password)
                server.sendmail(self.__sender_email, receiver, message)
        except (gaierror, ConnectionRefusedError):
            return 'Failed to connect to SMTP Server (Refused) '
        except smtplib.SMTPServerDisconnected:
            return 'Failed to connect to SMTP Server (Disconnected) '
        except smtplib.SMTPException as e:
            return 'SMTP error occurred: ' + str(e)
        return "Sent"

    def default_client(self):
        return EmailClient(self.__PORT, self.__SMTP_SERVER, self.__EMAIL_ADDRESS, self.__EMAIL_PASSWORD)

    # ----------------------------------------------------------------------------------------------------------------
