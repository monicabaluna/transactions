"""
Validator functions module.
@author Monica-Maria Baluna
"""

from datetime import datetime
import json
from flask import request

HTTP_ERROR_CODE = 400
MISSING_FIELD_TEMPLATE = 'Missing field \'{}\''
INVALID_FIELD_TEMPLATE = 'Invalid data for field \'{}\''

def is_date(date_string):
    """ Verifies if a string represents a date. """
    try:
        datetime.strptime(date_string, '%d-%m-%Y')
        return True
    except ValueError:
        return False

def is_positive_int(number_string):
    """ Verifies if a string represents a number. """
    try:
        return int(number_string) >= 0
    except ValueError:
        return False

def validate_request_data(request_method, request_attribute, field_validators):
    """
    Verifies if field values for a given request are correct.
    @param request_method - the request method (like GET or POST)
    @param request_attribute - request object attribute where data is stored
    @param field_validators - list of (field, validator) pairs
    """
    def validate_data(routing_handler):
        """ Decorates the routing_handler. """
        def decorated_handler(*args, **kwargs):
            """
            Validates fields and calls the routing handler if fields are valid.
            """
            if request.method != request_method:
                return routing_handler(*args, **kwargs)

            data = getattr(request, request_attribute)

            if not data:
                return routing_handler(*args, **kwargs)

            for field, validator in field_validators:
                value = data.get(field, None)
                if value is None:
                    return (json.dumps({'message':
                                        MISSING_FIELD_TEMPLATE.format(field)}),
                            HTTP_ERROR_CODE)

                if not validator(value):
                    return (json.dumps({'message':
                                        INVALID_FIELD_TEMPLATE.format(field)}),
                            HTTP_ERROR_CODE)

            return routing_handler(*args, **kwargs)

        # Flask uses function names internally to look for existing handlers,
        # so each decorated handler should have a unique name
        decorated_handler.__name__ = 'validated_' + routing_handler.__name__

        return decorated_handler

    return validate_data
