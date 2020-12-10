#!/usr/bin/env python3

from python_utils.sequence_utils import unpack_apply


capitalize = str.capitalize
upper = str.upper


def test_unpack_apply():
    x = ('bob', '33', 'fbi')
    res = unpack_apply(x, capitalize, int, upper)
    assert res == ('Bob', 33, 'FBI')


def test_unpack_apply_more_elements():
    x = ('bob', '33', 'fbi', 'banana')
    res = unpack_apply(x, capitalize, int, upper)
    assert res == ('Bob', 33, 'FBI', 'banana')


def test_unpack_apply_less_elements():
    x = ('bob', '33')
    res = unpack_apply(x, capitalize, int, upper)
    assert res == ('Bob', 33)


def test_unpack_apply_list():
    x = ['bob', '33', 'fbi']
    res = unpack_apply(x, capitalize, int, upper)
    assert res == ('Bob', 33, 'FBI')


def test_unpack_apply_from_string():
    x = 'bob 33 fbi'.split(' ')
    res = unpack_apply(x, capitalize, int, upper)
    assert res == ('Bob', 33, 'FBI')


def test_unpack_apply_generator():
    x = (_ for _ in ['bob', '33', 'fbi'])
    res = unpack_apply(x, capitalize, int, upper)
    assert res == ('Bob', 33, 'FBI')
