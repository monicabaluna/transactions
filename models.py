"""
Models for a mongodb database schema.
@author Monica-Maria Baluna
"""

from mongoengine import Document, IntField


class Transaction(Document):
    """ Transaction document model. """

    sender = IntField(required=True)
    receiver = IntField(required=True)
    amount = IntField(required=True)
    timestamp = IntField(required=True)
    meta = {
        'indexes': [
            ('sender', 'timestamp')
        ]
    }
