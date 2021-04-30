#!/usr/bin/env python3

"""
Created on 24 Mar 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sys.modem import ModemList


# --------------------------------------------------------------------------------------------------------------------
# run...

lines = [
    'modem-list.length   : 1',
    'modem-list.value[1] : /org/freedesktop/ModemManager1/Modem/0'
]

modems = ModemList.construct_from_mmcli(lines)
print(modems)

print('code:%s' % modems.modem_code(0))
