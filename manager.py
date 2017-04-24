"""
Manager for a mongodb transactions database.
@author Monica-Maria Baluna
"""

import json

from mongoengine.queryset.visitor import Q

from models import Transaction
from utils import get_timestamp


def add_transaction(sender, receiver, amount, timestamp):
    """
    Adds a transaction to the database.
    @param sender - integer representing sender id
    @param receiver - integer representing receiver id
    @param amount - integer representing sent amount
    @param timestamp - integer representing UNIX timestamp
    """
    Transaction.objects.insert([Transaction(sender=sender,
                                            receiver=receiver,
                                            amount=amount,
                                            timestamp=timestamp),
                                Transaction(sender=receiver,
                                            receiver=sender,
                                            amount=-amount,
                                            timestamp=timestamp)])

def search_transactions(user, day, threshold):
    """
    Searches for transactions performed by a user during a given day, over a
    given threshold.
    @param user - integer representing user id
    @param day - string representing a date
    @param threshold - integer representing minimum sent amount
    """
    start_ts = get_timestamp(day)
    seconds_a_day = 24 * 60 * 60
    end_ts = start_ts + seconds_a_day
    inverse_threshold = str(-int(threshold))

    result = []
    transactions = Transaction.objects(Q(sender=user) &
                                       Q(timestamp__gte=start_ts) &
                                       Q(timestamp__lt=end_ts) &
                                       (Q(amount__gt=threshold) |
                                        Q(amount__lt=inverse_threshold)))

    for transaction in transactions:
        element = json.loads(transaction.to_json())
        if '_id' in element:
            del element['_id']
        result.append(element)

    return result

def get_balance(user, since, until):
    """
    Computes a user's balance over a given time interval.
    @param user - integer representing user id
    @param since - string representing the start date
    @param until - string representing the end date
    """
    start_ts = get_timestamp(since)
    end_ts = get_timestamp(until)

    balance = -Transaction.objects(Q(sender=user) &
                                   Q(timestamp__gte=start_ts) &
                                   Q(timestamp__lt=end_ts)).sum('amount')

    return balance
