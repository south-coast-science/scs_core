#!/usr/bin/env python3

"""
Created on 14 Sep 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_log_cursor_queue import CSVLogCursorQueue


# --------------------------------------------------------------------------------------------------------------------

name = '2022-09'
is_valid = CSVLogCursorQueue.is_data_directory(name)
print("name: %s is_valid: %s" % (name, is_valid))

name = '0022-09'
is_valid = CSVLogCursorQueue.is_data_directory(name)
print("name: %s is_valid: %s" % (name, is_valid))

name = '2022-29'
is_valid = CSVLogCursorQueue.is_data_directory(name)
print("name: %s is_valid: %s" % (name, is_valid))

name = '2022-09-ignore'
is_valid = CSVLogCursorQueue.is_data_directory(name)
print("name: %s is_valid: %s" % (name, is_valid))

name = 'ignore-2022-09'
is_valid = CSVLogCursorQueue.is_data_directory(name)
print("name: %s is_valid: %s" % (name, is_valid))

name = 'YYYY-MM'
is_valid = CSVLogCursorQueue.is_data_directory(name)
print("name: %s is_valid: %s" % (name, is_valid))

