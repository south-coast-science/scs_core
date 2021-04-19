"""
Created on 07 Apr 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
import requests

from scs_core.estate.configuration import Configuration


class ConfigurationSearcher(object):
    __URL = "https://bwhogrzl3b.execute-api.us-west-2.amazonaws.com/default/MQTTDynamoHandler"

    def __init__(self):
        self.__data = None

    def get_data(self):
        data = requests.get(self.__URL)
        j_data = data.json()
        self.__data = j_data

    def get_by_name(self, name):
        include = []
        for item in self.__data:
            if name in item['device_tag']:
                x = Configuration.construct_from_jstr(item['data'])
                include.append(x)

        return include

