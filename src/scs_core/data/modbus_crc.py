"""
Created on 16 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Resources:
https://ctlsys.com/support/how_to_compute_the_modbus_rtu_message_crc/
"""


# --------------------------------------------------------------------------------------------------------------------

class ModbusCRC(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def compute(data):
        polynomial = 0xa001
        crc = 0xffff

        for datum in data:
            crc ^= datum

            for _ in range(8):
                if crc & 0x0001:
                    crc >>= 1
                    crc ^= polynomial

                else:
                    crc >>= 1

        return crc
