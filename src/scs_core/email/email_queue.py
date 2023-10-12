"""
Created on 28 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class EmailQueue(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        queue = jdict.get('queue')

        return EmailQueue(queue)

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, queue=None):
        """
        Constructor
        """
        self.__queue = queue

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['queue'] = self.__queue

        return jdict


    def pop_next(self):
        if self.__queue is None:
            return None, None

        json_list = self.as_json()
        queue = json_list.get("queue")

        if len(queue) < 1:
            return None, None
        key = list(queue)[0]
        value = queue.get(key)

        queue.pop(key)
        new_queue = json_list.get('queue')
        self.__queue = new_queue

        return key, value


    def add_item(self, device_tag, message):
        if self.__queue is None:
            self.__queue = {device_tag: message}
        else:
            self.__queue[device_tag] = message

        return self.__queue


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def queue(self):
        return self.__queue


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "EmailQueue:{Queue:%s }" % self.queue
