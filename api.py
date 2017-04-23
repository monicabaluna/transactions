"""
Server API module.
@author Monica-Maria Baluna
"""

import sys
import json
import logging

from flask import Flask, request
from mongoengine import connect

import manager
from utils import is_int, is_date, validate_data

HTTP_ERROR_CODE = 400

APP = Flask(__name__)
APP.config.from_object(__name__)

# Stop displaying received messages
LOG = logging.getLogger('werkzeug')
LOG.setLevel(logging.ERROR)

@APP.route('/transactions/', methods=['POST', 'GET'])
def handle_transactions():
    """ Build response for transactions page request. """
    if request.method == 'POST':
        data = request.json

        # test for valid fields
        message, valid = validate_data(data, [('sender', is_int),
                                              ('receiver', is_int),
                                              ('sum', is_int),
                                              ('timestamp', is_int)])
        if not valid:
            return json.dumps({'message': message}), HTTP_ERROR_CODE

        manager.add_transaction(data['sender'],
                                data['receiver'],
                                data['sum'],
                                data['timestamp'])

        return str(data['sender']) + " sent " + str(data['sum']) + "$ to " + \
        str(data['receiver'])

    # test for valid fields
    message, valid = validate_data(request.args, [('user', is_int),
                                                  ('day', is_date),
                                                  ('threshold', is_int)])
    if not valid:
        return json.dumps({'message': message}), HTTP_ERROR_CODE

    return str(manager.search_transactions(request.args['user'],
                                           request.args['day'],
                                           request.args['threshold']))

@APP.route('/balance/')
def get_balance():
    """ Build response for balance page request. """
    # test for valid fields
    message, valid = validate_data(request.args, [('user', is_int),
                                                  ('since', is_date),
                                                  ('until', is_date)])
    if not valid:
        return json.dumps({'message': message}), HTTP_ERROR_CODE

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
