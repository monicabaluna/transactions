"""
Server API module.
@author Monica-Maria Baluna
"""

import sys

from flask import Flask, request
from mongoengine import connect

import manager
from validators import is_positive_int, is_date, validate_request_data

APP = Flask(__name__)
APP.config.from_object(__name__)

@APP.route('/transactions/', methods=['POST', 'GET'])
@validate_request_data('POST', 'json', [('sender', is_positive_int),
                                        ('receiver', is_positive_int),
                                        ('sum', is_positive_int),
                                        ('timestamp', is_positive_int)])
@validate_request_data('GET', 'args', [('user', is_positive_int),
                                       ('day', is_date),
                                       ('threshold', is_positive_int)])
def handle_transactions():
    """ Build response for transactions page request. """
    if request.method == 'POST':
        data = request.json
        manager.add_transaction(data['sender'],
                                data['receiver'],
                                data['sum'],
                                data['timestamp'])

        return str(data['sender']) + " sent " + str(data['sum']) + "$ to " + \
        str(data['receiver'])

    # request method is GET
    return str(manager.search_transactions(request.args['user'],
                                           request.args['day'],
                                           request.args['threshold']))

@APP.route('/balance/', methods=['GET'])
@validate_request_data('GET', 'args', [('user', is_positive_int),
                                       ('since', is_date),
                                       ('until', is_date)])
def get_balance():
    """ Build response for balance page request. """
    balance = manager.get_balance(request.args['user'],
                                  request.args['since'],
                                  request.args['until'])
    return str(balance)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        connect('transactions_db_test', host='mongo', port=27017)

    else:
        connect('transactions_db', host='mongo', port=27017)

    print "Web server is active!"

    APP.run(host='0.0.0.0', debug=True)
