#!/usr/bin/env python3.8
'''
This module contains functions for working with dicts.
'''
import re

DETECT_CAMEL_RE = re.compile(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+')


def camel_to_snake(camel: str) -> str:
    '''Convert a camel cased string to snake case.'''
    words = DETECT_CAMEL_RE.findall(camel)
    return '_'.join(map(str.lower, words))


def snake_to_camel(snake: str) -> str:
    '''Convert a snake cased string to camel case.'''
    first, *others = snake.split('_')
    return ''.join([first.lower(), *map(str.title, others)])
