
"""
Performance testcases for the transactions API.
@author: Baluna Monica-Maria
"""

import unittest
import time
import random
import tempfile
import requests

from mongoengine import connect

import api
from models import Transaction
import manager
from utils import get_timestamp, next_date_string


HOME_URL = "http://127.0.0.1:5000/"
DAY_STRING1 = '10-03-2010'
DAY_STRING2 = '10-05-2010'

MAX_USERS = 300
MAX_SUM = 1000

NR_TESTS = 1000


class ApiPerformanceTestCase(unittest.TestCase):
    """ Class that implements the performance tests set behaviour."""

    def setUp(self):
        self.db_fd, api.APP.config['DATABASE'] = tempfile.mkstemp()
        api.APP.config['TESTING'] = True
        self.app = api.APP.test_client()
        connect('transactions_db_test')
        self.empty_db()
        self.fill_db()
        random.seed()

    def tearDown(self):
        self.empty_db()

    def fill_db(self):
        """ Add some data to the database. """
        ts_start = get_timestamp(DAY_STRING1)
        ts_end = get_timestamp(DAY_STRING2)

        for timestamp in range(ts_start, ts_end, 600):
            sender = random.randint(0, MAX_USERS)
            receiver = random.randint(0, MAX_USERS)
            sent_sum = random.randint(0, MAX_SUM)

            manager.add_transaction(sender, receiver, sent_sum, timestamp)

    def empty_db(self):
        """ Delete all data from the database. """
        Transaction.objects.delete()

    def test_add_entries(self):
        """ Test the POST performance for adding transactions to the database.
        """
        start_time = time.time()

        ts_start = get_timestamp(DAY_STRING1)
        ts_end = get_timestamp(DAY_STRING2)
        for _ in range(0, NR_TESTS):
            timestamp = random.randint(ts_start - 5000, ts_end + 5000)
            sender = random.randint(0, MAX_USERS)
            receiver = random.randint(0, MAX_USERS)
            sent_sum = random.randint(0, MAX_SUM)

            payload = {'sender': sender, 'receiver': receiver, 'sum': sent_sum,
                       'timestamp': timestamp}
            response = requests.post(HOME_URL + "transactions/", json=payload)
            assert response.status_code == 200

        end_time = time.time()
        print "\nPost transactions time: " + str(end_time - start_time)

    def test_get_transactions(self):
        """ Test the GET TRANSACTIONS performance - for listing user
            transactions over agiven threshold, in a given time interval.
        """
        start_time = time.time()

        for _ in range(0, NR_TESTS):
            user = random.randint(0, MAX_USERS)
            threshold = random.randint(0, MAX_SUM + 200)
            date_offset = random.randint(-10, 70)
            date = next_date_string(DAY_STRING1, date_offset)
            response = requests.get(HOME_URL + "transactions/?user=" +
                                    str(user) + "&day=" + date + "&threshold=" +
                                    str(threshold))
            assert response.status_code == 200

        end_time = time.time()
        print "\nGet transactions time: " + str(end_time - start_time)

    def test_balances(self):
        """ Test GET BALANCE performance - for computing a user's balance over
            a given time interval.
        """
        start_time = time.time()

        total_days = (get_timestamp(DAY_STRING2) -
                      get_timestamp(DAY_STRING1)) / 60 / 60 / 24

        for _ in range(0, NR_TESTS):
            user = random.randint(0, MAX_USERS)

            since_offset = random.randint(0, total_days / 2)
            until_offset = random.randint(total_days / 2, total_days)
            since = next_date_string(DAY_STRING1, since_offset)
            until = next_date_string(DAY_STRING1, until_offset)

            response = requests.get(HOME_URL + 'balance/?user=' + str(user) +
                                    '&since=' + since + '&until=' + until)
            assert response.status_code == 200

        end_time = time.time()
        print "\nGet balance time: " + str(end_time - start_time)

if __name__ == '__main__':
    unittest.main()
