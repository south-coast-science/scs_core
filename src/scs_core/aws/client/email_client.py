"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
"""
import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from socket import gaierror


# Unused (replaced by AWS SES)

# --------------------------------------------------------------------------------------------------------------------
class EmailClient(object):
    __PORT = 465
    __SMTP_SERVER = "smtp.gmail.com"

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def device_monitor_client(cls, device_monitor_conf):
        email_address = device_monitor_conf.email_name
        email_password = device_monitor_conf.email_password
        return EmailClient(cls.__PORT, cls.__SMTP_SERVER, email_address, email_password)

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, port=0, smtp_server="", login_address="", password=""):
        """
        Constructor
        """
        self.__port = port
        self.__smtp_server = smtp_server
        self.__sender_email = login_address
        self.__password = password
        self.__server = None

    # ----------------------------------------------------------------------------------------------------------------

    def open_server(self):
        # Should this go in the constructor?
        if not self.__port or not self.__smtp_server or not self.__sender_email or not self.__password:
            return "Email Client Not Configured"
        try:
            self.__server = smtplib.SMTP_SSL('%s: %s' % (self.__smtp_server, self.__port))
            self.__server.login(self.__sender_email, self.__password)
        except (gaierror, ConnectionRefusedError):
            return 'Failed to connect to SMTP Server (Refused) '
        except smtplib.SMTPServerDisconnected:
            return 'Failed to connect to SMTP Server (Disconnected) '
        except smtplib.SMTPException as e:
            return 'SMTP error occurred: ' + str(e)
        return "ok"

    def close_server(self):
        if not self.__server:
            return "No server open"
        self.__server.quit()

    def send_mime_email(self, message, device):
        if not self.__server:
            return "No server open"

        msg = MIMEMultipart()
        msg['From'] = self.__sender_email
        msg['To'] = self.__sender_email
        # TODO: Add extra recipients somewhere for each device
        msg['Subject'] = "SCS Device: %s" % device
        msg.attach(MIMEText(message))

        try:
            self.__server.sendmail(msg['From'], msg['To'], msg.as_string())
        except (gaierror, ConnectionRefusedError):
            return 'Failed to connect to SMTP Server (Refused) '
        except smtplib.SMTPServerDisconnected:
            return 'Failed to connect to SMTP Server (Disconnected) '
        except smtplib.SMTPException as e:
            return 'SMTP error occurred: ' + str(e)

        return True

    # ----------------------------------------------------------------------------------------------------------------
