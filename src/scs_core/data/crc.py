"""
Created on 16 Nov 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Resources:
https://ctlsys.com/support/how_to_compute_the_modbus_rtu_message_crc/

https://stackoverflow.com/questions/52391412/python-crc8-calculation
https://www.raspberrypi.org/forums/viewtopic.php?t=186576
"""


# --------------------------------------------------------------------------------------------------------------------

def modbus_crc(datagram):
    crc = 0xffff
    polynomial = 0xa001

    for datum in datagram:
        crc ^= datum

        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= polynomial
            else:
                crc >>= 1

    return crc


def crc8(datagram, crc=0xff, polynomial=0x31):
    for datum in datagram:
        for _ in range(8):
            if (datum ^ crc) & 0x80:
                crc <<= 1
                crc ^= polynomial
            else:
                crc <<= 1

            datum <<= 1

    return crc & 0xff
