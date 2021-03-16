'''Module with functions for accepting requests from AWS lambda.'''
import json
from typing import Optional, TypedDict

from aws_utils.exceptions import BadRequest


class PostRequest(TypedDict):
    '''Dict representing an AWS event from a POST request.'''
    body: Optional[str]


class GetRequest(TypedDict):
    '''Dict representing an AWS event from a GET request.'''
    pathParameters: Optional[dict]


def get_body_from_post_request(event: PostRequest):
    '''Get body from post request, and unmarshal the json value.

    Raise BadRequest if something is wrong.'''
    body_str: Optional[str] = event.get('body')

    if body_str is None:
        raise BadRequest('Missing request body')

    try:
        body = json.loads(body_str)
    except json.decoder.JSONDecodeError:
        raise BadRequest('Malformed json in request body')

    return body


def get_params_from_get_request(event: GetRequest):
    '''Get params from get request.

    Raise BadRequest if something is wrong.'''

    params = event.get('pathParameters')

    if params is None:
        raise BadRequest('Missing get parameters')

    return params
