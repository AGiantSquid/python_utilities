#!/usr/bin/env python3

from sequence_utils import unpack_apply


def test_unpack_apply():
    x = ('bob', '33', 'fbi')
    res = unpack_apply(x, lambda x: x.capitalize(), int, lambda x: x.upper())
    assert res == ('Bob', 33, 'FBI')


def test_unpack_apply_more_elements():
    x = ('bob', '33', 'fbi', 'banana')
    res = unpack_apply(x, lambda x: x.capitalize(), int, lambda x: x.upper())
    assert res == ('Bob', 33, 'FBI', 'banana')


def test_unpack_apply_less_elements():
    x = ('bob', '33')
    res = unpack_apply(x, lambda x: x.capitalize(), int, lambda x: x.upper())
    assert res == ('Bob', 33)


def test_unpack_apply_list():
    x = ['bob', '33', 'fbi']
    res = unpack_apply(x, lambda x: x.capitalize(), int, lambda x: x.upper())
    assert res == ('Bob', 33, 'FBI')


def test_unpack_apply_generator():
    x = (_ for _ in ['bob', '33', 'fbi'])
    res = unpack_apply(x, lambda x: x.capitalize(), int, lambda x: x.upper())
    assert res == ('Bob', 33, 'FBI')
