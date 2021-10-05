#!/usr/bin/env python3.8
'''
Module to verify iterable utils work.
'''

import pytest

from python_utils.dict_utils import coerce_datatypes


datatype_map = {
    'project': {
        'conversion_function': str,
    },
    'index': {
        'conversion_function': int,
        'default': 2,
    },
}


def test_coerce_datatypes():
    '''Convert a string to int'''
    data_to_coerce = {
        'project': 'hello',
        'index': '1',
    }

    res = coerce_datatypes(datatype_map, data_to_coerce)

    assert res == {
        'project': 'hello',
        'index': 1,
    }


def test_coerce_datatypes_2():
    '''Ignore a field'''
    data_to_coerce = {
        'project': 'hello',
        'index': '1',
        'extra_field': 'should get ignored'
    }

    res = coerce_datatypes(datatype_map, data_to_coerce)

    assert res == {
        'project': 'hello',
        'index': 1,
    }


def test_coerce_datatypes_3():
    '''Use a default value'''
    data_to_coerce = {
        'project': 'hello',
    }

    res = coerce_datatypes(datatype_map, data_to_coerce)

    assert res == {
        'project': 'hello',
        'index': 2,
    }


def test_coerce_datatypes_error():
    '''Omit a required value'''
    data_to_coerce = {
        'index': '1',
    }

    with pytest.raises(KeyError) as err:
        coerce_datatypes(datatype_map, data_to_coerce)

    assert err.value.args[1] == 'project'


def test_coerce_datatypes_error_2():
    '''use a value that cannot be converted'''
    data_to_coerce = {
        'project': 'hello',
        'index': 'hello',
    }

    with pytest.raises(ValueError) as err:
        coerce_datatypes(datatype_map, data_to_coerce)

    assert err.value.args[1] == ('index', 'hello')


def test_coerce_datatypes_error_3():
    '''use a value that cannot be converted'''
    data_to_coerce = {
        'project': 'hello',
        'index': None,
    }

    with pytest.raises(ValueError) as err:
        coerce_datatypes(datatype_map, data_to_coerce)

    assert err.value.args[1] == ('index', None)
