#!/usr/bin/env python3.8
'''
Module to demonstrate that string utils work.
'''
from python_utils.string_utils import camel_to_snake, snake_to_camel


def test_camel_to_snake():
    '''Check that camel cased strings get converted no legible snake case.'''
    tests = (
        ('camelCasedString', 'camel_cased_string'),
        ('HTTPRequest', 'http_request'),
        ('iCanCountTo9', 'i_can_count_to_9'),
        ('myJSONString', 'my_json_string'),
    )

    for test, expected in tests:
        res = camel_to_snake(test)
        assert res == expected


def test_snake_to_camel():
    '''Check that snake cased strings get converted to legible camel case.'''
    tests = (
        ('snake_cased_string', 'snakeCasedString'),
        ('http_request', 'httpRequest'),
        ('i_can_count_to_9', 'iCanCountTo9'),
        ('my_json_string', 'myJsonString'),
    )

    for test, expected in tests:
        res = snake_to_camel(test)
        assert res == expected
