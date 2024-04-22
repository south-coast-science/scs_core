"""
Created on 11 Apr 2024

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{'device': 'scs-opc-261', 'topic': 'southtyneside/cube/loc/261/gases', 'rec': '2024-04-11T11:12:05Z',
'lastSeenTime': '2024-04-11T17:00:11Z', 'message': {'exg': {'cnc': Decimal('24.8'), 'src': 'oE.1'},
'val': {'tmp': Decimal('19.7'), 'hmd': Decimal('55.3'), 'vCal': Decimal('75.5'), 'cnc': Decimal('28'),
'weC': Decimal('0.04051'), 'aeV': Decimal('0.27751'), 'weV': Decimal('0.30016')}, 'src': 'SD1',
'ver': Decimal('2'), 'tag': 'scs-opc-261', 'rec': '2024-04-11T11:12:05Z'}}
"""

from scs_core.aws.data.ingestion.ingestible_message import IngestibleMessage
from scs_core.aws.manager.byline.byline import Byline


# --------------------------------------------------------------------------------------------------------------------

class IngestibleByline(Byline):
    """
    classdocs
    """

    @classmethod
    def construct_from_message(cls, message: IngestibleMessage):
        return cls(message.device, message.topic, message.rec_at, message.upload, message.payload)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device, topic, rec, pub, message):
        """
        Constructor
        """
        super().__init__(device, topic, rec, pub, message)


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        rec = self.rec.as_iso8601()

        jdict = {
            'device': self.device,
            'topic': self.topic,
            'last_write': rec,
            'lastSeenTime': self.pub.as_iso8601(include_millis=True),
            'message': self.message,
            'rec': rec
        }

        return jdict
