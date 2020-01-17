#!/usr/bin/env python3

"""
Created on 14 Jan 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.csv.csv_log import CSVLog
from scs_core.csv.csv_log_reader import CSVLogReader
from scs_core.csv.csv_logger_conf import CSVLoggerConf
from scs_core.csv.csv_reader import CSVReaderException

from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.data.publication import Publication

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

start_iso = '2019-01-25T13:37:00Z'
topic_name = 'gases'

start = LocalizedDatetime.construct_from_iso8601(start_iso)
start_datetime = start.datetime

print("start_datetime: %s" % start_datetime)
print("-")

conf = CSVLoggerConf.load(Host)
print(conf)

log = CSVLog(conf.root_path, topic_name, None, start)
print(log)

reader = CSVLogReader(log)
print(reader)

print("-")

for file in reader.log_files():
    print(file)

    try:
        for datum in reader.documents(file, 'rec'):
            publication = Publication(file.topic_name, datum)
            print(json.dumps(publication.as_json()))

    except CSVReaderException:
        print("skipping file")
