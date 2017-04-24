"""
Utility functions module.
@author Monica-Maria Baluna
"""

from datetime import datetime, timedelta

def get_timestamp(date_string):
    """
    Get UNIX timestamp for the start of a day.
    @param date_string -  string representing a day
    """
    start_moment = datetime.strptime(date_string, '%d-%m-%Y')
    delta_utctime = start_moment - datetime.utcfromtimestamp(0)
    return int(delta_utctime.total_seconds())

def is_date(date_string):
    """ Validator. Verifies if a string represents a date. """
    try:
        datetime.strptime(date_string, '%d-%m-%Y')
        return True
    except ValueError:
        return False

def is_positive_int(number_string):
    """ Validator. Verifies if a string represents a number. """
    try:
        return int(number_string) >= 0
    except ValueError:
        return False

def validate_data(data, validator_pairs):
    """
    Validator. Receives a collection of key-value pairs and a list of validator
    functions (one for each key) and checks that all values are valid for their
    respective keys.
    """
    for field, validator in validator_pairs:
        value = data.get(field, None)
        if value is None:
            return 'missing field \'%s\'' % field, False
        if not validator(value):
            return 'invalid field \'%s\': ' % field + str(value), False
    return '', True

def next_date_string(date_string, offset):
    """
    Adds days do a date and returns the result.
    @param date_string - string representing a date
    @param offset - number of days to add
    """
    date = datetime.strptime(date_string, '%d-%m-%Y')
    date += timedelta(days=offset)
    return datetime.strftime(date, '%d-%m-%Y')
