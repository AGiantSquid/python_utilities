'''Module with functions for returning responses from AWS lambda.'''
import json
import logging
import traceback
from functools import wraps
from http import HTTPStatus
from typing import TypedDict, Optional

from aws_utils.http_exceptions import BadRequest, InternalServerError, ServerError
from python_utils.json_utils import decimal_default

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


def success_response(payload) -> Response:
    '''Returns 200 response with payload serialized as json.'''
    LOGGER.info('Success response: %s', payload)

    body = json.dumps(payload, default=decimal_default)

    return http_response(body, HTTPStatus.OK)


def bad_request(err: BadRequest) -> Response:
    '''Returns a 400 response with the error message.'''
    return error_response(err, HTTPStatus.BAD_REQUEST)


def internal_server_error(err: InternalServerError) -> Response:
    '''Returns a 500 response with error message.'''
    return error_response(err, HTTPStatus.INTERNAL_SERVER_ERROR)


def error_response(err: ServerError, status: HTTPStatus) -> Response:
    '''Returns response for errors.'''
    LOGGER.exception(err)

    errors = err.errors if err.errors else []

    body = json.dumps({
        'code': status.value,
        'message': err.message,
        'errors': errors,
    }, default=decimal_default)

    return http_response(body, status)


def http_response(
        body: str,
        status: HTTPStatus = HTTPStatus.OK,
        headers: Optional[dict] = None,
    ) -> Response:
    '''Returns http response for lambda.'''
    if headers is None:
        headers = DEFAULT_HEADERS

    return {
        'body': body,
        'statusCode': status.value,
        'headers': headers,
    }


def handle_exceptions(func):
    '''Decorator to handle all unhandled exceptions in a lambda.

    If you do not handle an exception in a lambda, the front end gets a CORS error.
    This returns the last line of the python exception to aid in debugging for any
    unspecified errors.'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            exc = InternalServerError(
                'unhandled internal error',
                errors=[traceback.format_exc(1)]
            )

            return internal_server_error(exc)

    return wrapper
