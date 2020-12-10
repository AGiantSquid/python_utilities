#!/usr/bin/env python3.8
'''
This module contains functions for working with dicts.
'''
import re

DETECT_CAMEL_RE = re.compile(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+')


def camel_to_snake(camel_str):
    '''Convert a camel cased string to snake case.'''
    words = DETECT_CAMEL_RE.findall(camel_str)
    return '_'.join(map(str.lower, words))


def snake_to_camel(snake_str):
    '''Convert a snake cased string to camel case.'''
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])
