#!/usr/bin/env python3.8
'''
Useful functions to work with iterables.
'''
from functools import reduce
from typing import Any, Callable, Iterable, Tuple


def divide(subject: Iterable, filter_func: Callable[[Any], bool]):
    '''Divide an iterable into 2 tuples according to filter func.

    The first tuple contains all elements that match the filter,
    the second contains those that do not.
    '''
    # Tuple that can have any length
    VaribleTuple = Tuple[Any, ...]

    def reducer_func(accum: Tuple[VaribleTuple, VaribleTuple], el):
        if filter_func(el):
            return (*accum[0], el), accum[1]

        return accum[0], (*accum[1], el)

    return reduce(reducer_func, subject, ((), ()))
