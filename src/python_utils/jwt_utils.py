#!/usr/bin/env python3.9
'''
Module for dealing with JWT tokens.
'''

import base64
import json


def get_jwt_token_components(encoded_jwt):
    '''Return the type, header, payload, and signature from the jwt.'''
    jwt_type, jwt_string = encoded_jwt.split(' ')

    header, payload, signature = jwt_string.split('.', 2)

    return {
        'jwt_type': jwt_type,
        'jwt_header': decode_jwt_component(header),
        'jwt_payload': decode_jwt_component(payload),
        'jwt_signature': signature,
    }


def decode_jwt_component(encoded_jwt):
    '''Suffix encoded string with "=" signs, and base64 decode.'''
    # python b64 decoding requires the string have multiple of 4 chars in string,
    # so add "=" signs until it has enough chars
    encoded_with_padding = encoded_jwt + '=' * (4 - len(encoded_jwt) % 4)
    decoded = base64.urlsafe_b64decode(encoded_with_padding).decode('utf-8')
    return json.loads(decoded)
