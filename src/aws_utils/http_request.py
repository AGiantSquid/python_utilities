'''Module with functions for accepting requests from AWS lambda.'''
import json
from typing import Optional

from exceptions import BadRequest


def get_body_from_post_request(event: dict):
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
