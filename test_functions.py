"""
Testcases for the transactions API.
@author: Baluna Monica-Maria
"""

import unittest
import time
from collections import defaultdict
import requests

from mongoengine import connect

from models import Transaction
import manager
from utils import get_timestamp


HOME_URL = "http://127.0.0.1:5000/"
DAY_STRING1 = '10-03-2010'
DAY_STRING2 = '13-03-2010'

MAX_USERS = 100
MAX_SUM = 200

HTTP_ERROR_CODE = 400
HTTP_SUCCESS_CODE = 200


class ApiTestCase(unittest.TestCase):
    """ Class that implements the tests set behaviour."""

    def setUp(self):
        self.balance = defaultdict(int)
        connect('transactions_db_test', host='mongo', port=27017)
        self.empty_db()
        self.fill_db()

    def tearDown(self):
        self.empty_db()

    def fill_db(self):
        """ Add some data to the database. """
        ts_start = get_timestamp(DAY_STRING1)
        ts_end = get_timestamp(DAY_STRING2)

        user = 1
        sent_sum = 101
        for timestamp in range(ts_start, ts_end, 1200):
            sender = user
            receiver = user % MAX_USERS + 1

            manager.add_transaction(sender, receiver, sent_sum, timestamp)

            self.balance[sender] -= sent_sum
            self.balance[receiver] += sent_sum

            user = user % MAX_USERS + 1
            sent_sum = sent_sum % MAX_SUM + 1

    def empty_db(self):
        """ Delete all data from the database. """
        Transaction.objects.delete()

    def test_add_entry(self):
        """ Test the POST method for adding transactions to the database. """
        payload = {'sender': 3, 'receiver': 4, 'sum': 25,
                   'timestamp': time.time()}
        response = requests.post(HOME_URL + "transactions/", json=payload)
        assert '3 sent 25$ to 4' in response.text
        assert response.status_code == HTTP_SUCCESS_CODE

    def test_add_entry_less_args(self):
        """ Test WRONG POST method call - missing fields"""
        payload = {'sender': 3, 'sum': 25, 'timestamp': time.time()}
        response = requests.post(HOME_URL + "transactions/", json=payload)
        assert response.status_code == HTTP_ERROR_CODE

    def test_add_entry_wrong_sum(self):
        """ Test WRONG POST method call - wrong sum"""
        payload = {'sender': 3, 'receiver': 4, 'sum': 'drop tables',
                   'timestamp': time.time()}
        response = requests.post(HOME_URL + "transactions/", json=payload)
        assert response.status_code == HTTP_ERROR_CODE

    def test_add_entry_wrong_time(self):
        """ Test WRONG POST method call - wrong timestamp"""
        payload = {'sender': 3, 'receiver': 4, 'sum': 7, 'timestamp': -1}
        response = requests.post(HOME_URL + "transactions/", json=payload)
        assert response.status_code == HTTP_ERROR_CODE

    def test_add_entry_wrong_sender(self):
        """ Test WRONG POST method call - wrong sender"""
        payload = {'sender': 'Monica', 'receiver': 4, 'sum': 7, 'timestamp': 3}
        response = requests.post(HOME_URL + "transactions/", json=payload)
        assert response.status_code == HTTP_ERROR_CODE

    def test_add_entry_wrong_receiver(self):
        """ Test WRONG POST method call - wrong receiver"""
        payload = {'sender': 3, 'receiver': 'X', 'sum': 7, 'timestamp': 3}
        response = requests.post(HOME_URL + "transactions/", json=payload)
        assert response.status_code == HTTP_ERROR_CODE

    def test_get_transactions(self):
        """ Test the GET TRANSACTIONS method - for listing user transactions
            over agiven threshold, in a given time interval.
        """
        response = requests.get(HOME_URL + "transactions/?user=1&day=" +
                                DAY_STRING1 + "&threshold=14")
        bad_ts = get_timestamp(DAY_STRING2) + 1
        good_ts = get_timestamp(DAY_STRING1)

        assert response.status_code == HTTP_SUCCESS_CODE
        assert 'sender":', u'2' in response.text
        assert 'receiver":', u'2' in response.text
        assert 'sender":', u'1' in response.text
        assert 'receiver":', u'3' in response.text
        assert 'sender":', u'3' not in response.text
        assert 'receiver":', u'1' not in response.text
        assert 'amount":', u'13' not in response.text
        assert ("timestamp': " + str(bad_ts)) not in response.text
        assert "timestamp': " + str(good_ts) in response.text

    def test_get_transactions_less_args(self):
        """ Test WRONG GET TRANSACTIONS method call - missing fields. """
        response = requests.get(HOME_URL +
                                "transactions/?user=12&threshold=14")
        assert response.status_code == HTTP_ERROR_CODE

    def test_get_transactions_wrong_user(self):
        """ Test WRONG GET TRANSACTIONS method call - wrong user. """
        response = requests.get(HOME_URL + "transactions/?user=abc&day=" +
                                DAY_STRING1 + "&threshold=14")
        assert response.status_code == HTTP_ERROR_CODE

    def test_get_transactions_wrong_day(self):
        """ Test WRONG GET TRANSACTIONS method call - wrong day. """
        response = requests.get(HOME_URL + "transactions/?user=1&day=3-06" +
                                "&threshold=14")
        assert response.status_code == HTTP_ERROR_CODE

    def test_get_transactions_wrong_threshold(self):
        """ Test WRONG GET TRANSACTIONS method call - wrong threshold. """
        response = requests.get(HOME_URL + "transactions/?user=1&day=" +
                                DAY_STRING1 + "&threshold=-14")
        assert response.status_code == HTTP_ERROR_CODE

    def test_balance(self):
        """ Test GET BALANCE method - for computing a user's balance over a
            given time interval.
        """
        for user in range(0, MAX_USERS):
            response = requests.get(HOME_URL + "balance/?user=" + str(user) +
                                    "&since=" + DAY_STRING1 + "&until=" +
                                    DAY_STRING2)
            assert response.text == str(self.balance[user])
            assert response.status_code == HTTP_SUCCESS_CODE

    def test_balance_missing_days(self):
        """ Test WRONG GET BALANCE method call - missing day fields. """
        response = requests.get(HOME_URL + "balance/?user=12")
        assert response.status_code == HTTP_ERROR_CODE

    def test_balance_missing_user(self):
        """ Test WRONG GET BALANCE method call - missing user field. """
        response = requests.get(HOME_URL + "balance/?since=" + DAY_STRING1 +
                                "&until=" + DAY_STRING2)
        assert response.status_code == HTTP_ERROR_CODE

    def test_bad_balance_wrong_date(self):
        """ Test WRONG GET BALANCE method call - wrong date value. """
        response = requests.get(HOME_URL + 'balance/?user=12&since=103-2017' +
                                '&until=10-04-2017')
        assert response.status_code == HTTP_ERROR_CODE

    def test_bad_balance_wrong_user(self):
        """ Test WRONG GET BALANCE method call - wrong user value. """
        response = requests.get(HOME_URL +
                                'balance/?user=1.2&since=03-03-2017' +
                                '&until=10-04-2017')
        assert response.status_code == HTTP_ERROR_CODE

    def test_invalid_post(self):
        """ Test invalid POST method. """
        payload = {'sender': 3, 'receiver': 4, 'sum': 25,
                   'timestamp': time.time()}
        response = requests.post(HOME_URL + "transactions/", data=payload)
        assert response.status_code == HTTP_ERROR_CODE


if __name__ == '__main__':
    unittest.main()
