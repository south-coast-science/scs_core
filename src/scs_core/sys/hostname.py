"""
Created on 4 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""


# --------------------------------------------------------------------------------------------------------------------

class Hostname(object):
    """
    classdocs
    """

    __HOSTNAME_FILE =       "/etc/hostname"                 # hard-coded path
    __HOSTS_FILE =          "/etc/hosts"                    # hard-coded path


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def is_valid_serial_number(cls, serial_number):
        try:
            int(serial_number)
            return True
        except (TypeError, ValueError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, prefix, serial_number):
        """
        Constructor
        """
        self.__prefix = prefix                              # string
        self.__serial_number = serial_number                # int-like string (may have leading zeroes)


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        # existing...
        with open(self.__HOSTNAME_FILE, 'r') as f:
            existing_hostname = f.read().strip()

        # hosts...
        with open(self.__HOSTS_FILE, 'r') as f:
            hosts = f.read()

        if existing_hostname not in hosts:
            raise ValueError(existing_hostname)

        with open(self.__HOSTS_FILE, 'w') as f:
            f.write(hosts.replace(existing_hostname, self.new_hostname))

        # hostname...
        with open(self.__HOSTNAME_FILE, 'w') as f:
            print(self.new_hostname, file=f)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def serial_number(self):
        return self.__serial_number


    @property
    def new_hostname(self):
        return self.__prefix + self.__serial_number


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Hostname:{prefix:%s, serial_number:%s}" % (self.__prefix, self.__serial_number)
