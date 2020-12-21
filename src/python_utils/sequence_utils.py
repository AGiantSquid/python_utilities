#!/usr/bin/env python3.8
'''
Useful functions to work with iterables.
'''
from typing import Sequence


def unpack_apply(iterable_input: Sequence, *args) -> tuple:
    '''Apply a sequence of functions to elements in a sequence by index.

    >>> x = 'bob 33 fbi'
    >>> unpack_apply(x.split(' '), str.capitalize, int, str.upper)
    ('Bob', 33, 'FBI')
    '''
    try:
        iterable_input[0]
        input_sequence = iterable_input
    except TypeError:
        input_sequence = list(iterable_input)

    applied = (_[1](_[0]) if _[1] else _[0] for _ in zip(input_sequence, args))

    rest = input_sequence[len(args):]

    return (*applied, *rest)
