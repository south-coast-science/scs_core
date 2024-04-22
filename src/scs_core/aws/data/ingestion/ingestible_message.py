"""
Created on 11 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example source:
{
    "payload": {
        "exg": {
            "cnc": 24.8,
            "src": "oE.1"
        },
        "val": {
            "tmp": 19.7,
            "hmd": 55.3,
            "vCal": 75.5,
            "cnc": 28,
            "weC": 0.04051,
            "aeV": 0.27751,
            "weV": 0.30016
        },
        "src": "SD1",
        "ver": 2,
        "tag": "scs-opc-261",
        "rec": "2024-04-11T11:12:05Z"
    },
    "topic": "southtyneside/cube/loc/261/gases",
    "client": "scs-cube-261-core-c00"
}

example document:
{'device': 'scs-opc-261', 'topic': 'southtyneside/cube/loc/261/gases', 'upload': '2024-04-11T16:59:18Z',
'rec_at': '2024-04-11T11:12:05Z', 'expire_at': Decimal('1712920325'),
'payload': {'exg': {'cnc': Decimal('24.8'), 'src': 'oE.1'}, 'val': {'tmp': Decimal('19.7'),
'hmd': Decimal('55.3'), 'vCal': Decimal('75.5'), 'cnc': Decimal('28'), 'weC': Decimal('0.04051'),
'aeV': Decimal('0.27751'), 'weV': Decimal('0.30016')}, 'src': 'SD1', 'ver': Decimal('2'),
'tag': 'scs-opc-261', 'rec': '2024-04-11T11:12:05Z'}}
"""

import pytz

from scs_core.aws.data.message import Message
from scs_core.data.datetime import LocalizedDatetime


# --------------------------------------------------------------------------------------------------------------------

class IngestibleMessage(Message):
    """
    classdocs
    """

    EXCLUDED_TOPIC_SUFFIX = '/control'

    TIMEZONE = pytz.timezone('Etc/UTC')

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_publication_jdict(cls, jdict):
        if not jdict:
            return None

        if jdict.get('client') == 'N/A':            # AWS IoT shadow message
            return None

        topic = jdict.get('topic')
        payload = jdict.get('payload')

        if not payload:
            return None

        device = payload.get('tag')
        upload = LocalizedDatetime.now(tz=cls.TIMEZONE)
        rec_at = LocalizedDatetime.construct_from_iso8601(payload.get('rec'))

        return cls(device, topic, upload, payload, rec_at, None)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, topic, upload, payload, rec_at, expire_at):
        """
        Constructor
        """
        super().__init__(device, topic, upload, payload)

        self.__rec_at = rec_at                                  # LocalizedDatetime
        self.__expire_at = expire_at                            # LocalizedDatetime or None


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        return self.device is not None and self.topic is not None and self.upload is not None and \
            self.payload is not None and self.rec_at is not None


    def is_excluded(self):
        return self.topic.endswith(self.EXCLUDED_TOPIC_SUFFIX)


    def set_ttl(self, ttl):
        self.__expire_at = None if ttl is None else self.rec_at + ttl


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = {
            'device': self.device,
            'topic': self.topic,
            'upload': self.upload.as_iso8601(include_millis=True),
            'rec_at': self.rec_at.as_iso8601(),
            'expire_at': None if self.expire_at is None else int(self.expire_at.timestamp()),
            'payload': self.payload
        }

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def rec_at(self):
        return self.__rec_at


    @property
    def expire_at(self):
        return self.__expire_at


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IngestibleMessage:{device:%s, topic:%s, upload:%s, rec_at:%s, expire_at:%s, payload:%s}" % \
               (self.device, self.topic, self.upload, self.rec_at, self.expire_at, self.payload)
