"""
Created on 07 Apr 2020

@author: Jade Page (jade.page@southcoastscience.com)

Really simple test script to grab the configuration data stored in the cloud
"""

from scs_core.estate.config_search import ConfigurationSearcher

cs = ConfigurationSearcher()
cs.get_data()
x = cs.get_by_name("opc")
print(x)

