'''Module with functions for returning responses from AWS lambda.'''
import json
import logging
from decimal import Decimal
from typing import TypedDict, Optional

from aws_utils.exceptions import BadRequest, InternalServerError, ServerError


LOGGER = logging.getLogger(__file__)
DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'OPTIONS,POST',
}


class Response(TypedDict):
    '''Response object AWS expects all proxy lambdas to return.'''
    statusCode: int
    headers: dict
    body: str  # body is a json string


def decimal_default(obj):
    '''Needed to get default json library to correctly parse Decimal objects.
    See the following for more detail:
    https://stackoverflow.com/questions/16957275/python-to-json-serialization-fails-on-decimal/16957370#16957370
    '''
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" %
                    type(obj).__name__)


def success_response(payload) -> Response:
    '''Returns 200 response with payload serialized as json.'''
    LOGGER.info('200 response: %s', payload)

    body = json.dumps(payload, default=decimal_default)

    return http_response(body, 200)


def bad_request(err: BadRequest) -> Response:
    '''Returns a 400 response with the error message.'''
    return error_response(err, 400)


def internal_server_error(err: InternalServerError) -> Response:
    '''Returns a 500 response with error message.'''
    return error_response(err, 500)


def error_response(err: ServerError, code: int) -> Response:
    '''Returns response for errors.'''
    LOGGER.exception(err)

    errors = err.errors if err.errors else []

    body = json.dumps({
        'code': code,
        'message': err.message,
        'errors': errors,
    }, default=decimal_default)

    return http_response(body, code)


def http_response(body: str, code=200, headers: Optional[dict] = None) -> Response:
    '''Returns http response for lambda.'''
    if headers is None:
        headers = DEFAULT_HEADERS

    return {
        'body': body,
        'statusCode': code,
        'headers': headers,
    }
