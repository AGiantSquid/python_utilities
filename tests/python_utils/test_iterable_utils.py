#!/usr/bin/env python3.8
'''
Module to verify iterable utils work.
'''
from python_utils.iterable_utils import partition


def test_partition():
    input_list = [1, 2, 3, 4, 5, 2, 3, 5, 8]

    less_than_three = lambda x: x < 3

    less, more = partition(input_list, less_than_three)

    assert less == (1, 2, 2)
    assert more == (3, 4, 5, 3, 5, 8)


def test_partition_types():
    input_list = [1, 'bob', 3, 'janet', 5, 8]

    is_string = lambda x: isinstance(x, str)

    strings, not_strings = partition(input_list, is_string)

    assert strings == ('bob', 'janet')
    assert not_strings == (1, 3, 5, 8)
