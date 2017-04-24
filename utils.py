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

def next_date_string(date_string, offset):
    """
    Adds days do a date and returns the result.
    @param date_string - string representing a date
    @param offset - number of days to add
    """
    date = datetime.strptime(date_string, '%d-%m-%Y')
    date += timedelta(days=offset)
    return datetime.strftime(date, '%d-%m-%Y')
