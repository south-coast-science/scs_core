#!/usr/bin/env python3

"""
Created on 1 Mar 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.datum import Datum


# --------------------------------------------------------------------------------------------------------------------

url = 'https://www.bbc.co.uk/news'
print("url: %s valid: %s" % (url, Datum.is_url(url)))


url = 'www.bbc.co.uk/news'
print("url: %s valid: %s" % (url, Datum.is_url(url)))

