#!/usr/bin/env python3

"""
Created on 23 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.csv.csv_log_cursor_queue import CSVLogCursorQueue, CSVLogCursor


# --------------------------------------------------------------------------------------------------------------------

queue = CSVLogCursorQueue()
print(queue)
print("-")

cursor = CSVLogCursor("a/b/c/3", 0, True)
queue.include(cursor)

cursor = CSVLogCursor("a/b/c/1", 23, False)
queue.include(cursor)

cursor = CSVLogCursor("a/b/c/2", 0, False)
queue.include(cursor)

print(queue)
print("-")

cursor = queue.next()
queue.remove(cursor.file_path)
print(cursor)

cursor = queue.next()
queue.remove(cursor.file_path)
print(cursor)

cursor = queue.next()
queue.remove(cursor.file_path)
print(cursor)
print("-")

cursor = queue.next()
print(cursor)
